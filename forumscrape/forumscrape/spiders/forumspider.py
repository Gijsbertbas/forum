import scrapy
from scrapy.shell import inspect_response
from forumscrape.items import ForumDjangoItem, ForumMissingItem
from datetime import datetime
import os
from forum.models import ForumMessageModel
import re

class ForumMessageSpider(scrapy.Spider):
    '''
    Inspect a single message.
    Used to find the right xpath syntax to scape the pages.
    Use the message id as argument to the spider:
    scrapy crawl inspectforummessage -a mid=....
    The response will be available in the terminal. 
    Finish with CRL+D
    '''

    name = 'inspectforummessage'

    def __init__(self, mid='', *args, **kwargs):
        super(ForumMessageSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.network54.com/Forum/95272/message/%s' % mid]

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'username': os.environ['FORUMUSER'], 'password': os.environ['FORUMPASSWORD']},
            callback=self.after_login
        )

    def after_login(self, response):
        inspect_response(response, self) # opens terminal
        return

class ForumLoginSpider(scrapy.Spider):
    '''
    Scrape # number of index pages. 
    Specific index pages or range are defined below.
    '''
    name = 'scrapeforum'
    start_urls = ['http://www.network54.com/Forum/95272']
    download_timeout = 20

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'username': os.environ['FORUMUSER'], 'password': os.environ['FORUMPASSWORD']},
            callback=self.after_login
        )

    def after_login(self, response):

        indices = [243,244,245,246,247,248,249]
        for i in indices:
            yield scrapy.Request('http://www.network54.com/Forum/95272/page-%s' % i, callback=self.get_parents)

    def get_parents(self, response):

        parents = response.xpath('//table[@cellspacing=1]//td[not(contains(.,"\xa0"))]//a/@href').extract()

        for parent in parents:
            request = scrapy.Request(parent, callback=self.process_message)
            request.meta['parentID'] = None
            yield request

    def process_message(self, response):
        item = ForumDjangoItem()

        item['title'] = response.xpath('//h1/text()').extract_first()
        item['author'] = response.xpath('//h1/following-sibling::text()').re_first(r'by\s([^\(]+)').strip()
        body = ''.join(response.xpath('//div[@class="intelliTxt KonaBody"]').extract())
        item['body'] = re.sub('<!-- google_ad_section_end -->','',body[65:-6]) # remove div and google tags
        item['bodylen'] = len(item['body'])
        item['timestamp'] = datetime.strptime(response.xpath('//i/text()').re_first(r'Geplaatst op\s*(.*)'),'%b %d, %Y, %I:%M %p')
        item['n54ID'] = response.url.split("/")[-2]
        item['n54URL'] = response.url
        item['parentID'] = response.meta['parentID']

        children = response.xpath('//table[@cellspacing=1]//td[not(contains(.,"\xa0"))]//a/@href').extract()
        # if no children this returns an empty list

        yield item

        for child in children:
            request = scrapy.Request(child, callback=self.process_message)
            request.meta['parentID'] = item['n54ID']
            yield request

class ForumCheckSpider(scrapy.Spider):
    '''
    This spider checks which posts are still missing in the local database.
    To run, cancel the pipeline and run with:
    scrapy crawl checkmissingposts -t csv -o missing.csv --loglevel=INFO
    '''
    
    name = 'checkmissingposts'
    start_urls = ['http://www.network54.com/Forum/95272']
    download_timeout = 20
    download_delay = 2

    def __init__(self, *args, **kwargs):
        super(ForumCheckSpider, self).__init__(*args, **kwargs)
        self.ids_seen = ForumMessageModel.objects.all().values_list('n54ID',flat=True)


    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'username': os.environ['FORUMUSER'], 'password': os.environ['FORUMPASSWORD']},
            callback=self.after_login
        )

    def after_login(self, response):

        for i in range(1,422):
            yield scrapy.Request('http://www.network54.com/Forum/95272/page-%s' % i, callback=self.get_parents)

    def get_parents(self, response):

        item = ForumMissingItem()
        item['indexpage']=response.url

        posts = response.xpath('//table[@cellspacing=1]//a/@href').extract()
        ids = []

        for post in posts:
            n54ID = post.split("/")[-2]

            if not int(n54ID) in self.ids_seen:
                ids.append(n54ID)

        item['postids'] = ids
        yield item

class ForumInfillSpider(scrapy.Spider):
    '''
    This spider is used to fill in missing posts.
    Mainly caused by posts with titels like '..' or '.'
    The original links which include the titel in the URL gave an error and could not be scraped.
    But because URLs with only the message id did work (excluding the titel in the url)
    I could 'fill in' the missing posts this way.
    The spider scrapes the missing message and its descendents.
    Run by:
    scrapy crawl foruminfill -a message=... [-a parent=...] 
    The parent argument only for messages which are children themselves.
    '''
    
    name = 'foruminfill'
    start_urls = ['http://www.network54.com/Forum/95272']
    download_timeout = 20

    def __init__(self, message='', parent=None, *args, **kwargs):
        super(ForumInfillSpider, self).__init__(*args, **kwargs)
        self.message = message
        self.parent = parent

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'username': os.environ['FORUMUSER'], 'password': os.environ['FORUMPASSWORD']},
            callback=self.after_login
        )

    def after_login(self, response):

        message = ['http://www.network54.com/Forum/95272/message/%s' % self.message]

        request = scrapy.Request(message[0], callback=self.process_message)
        request.meta['parentID'] = self.parent
        yield request

    def process_message(self, response):
        item = ForumDjangoItem()

        item['title'] = response.xpath('//h1/text()').extract_first()
        item['author'] = response.xpath('//h1/following-sibling::text()').re_first(r'by\s([^\(]+)').strip()
        body = ''.join(response.xpath('//div[@class="intelliTxt KonaBody"]').extract())
        item['body'] = re.sub('<!-- google_ad_section_end -->','',body[65:-6]) # remove div and google tags
        item['bodylen'] = len(item['body'])
        item['timestamp'] = datetime.strptime(response.xpath('//i/text()').re_first(r'Geplaatst op\s*(.*)'),'%b %d, %Y, %I:%M %p')
        item['n54ID'] = response.url.split("/")[-1]
        item['n54URL'] = response.url
        item['parentID'] = response.meta['parentID']

        children = response.xpath('//table[@cellspacing=1]//td[not(contains(.,"\xa0"))]//a/@href').extract()

        yield item

        for child in children:
            request = scrapy.Request(child, callback=self.process_children)
            request.meta['parentID'] = item['n54ID']
            yield request

    def process_children(self, response):
        item = ForumDjangoItem()

        item['title'] = response.xpath('//h1/text()').extract_first()
        item['author'] = response.xpath('//h1/following-sibling::text()').re_first(r'by\s([^\(]+)').strip()
        body = ''.join(response.xpath('//div[@class="intelliTxt KonaBody"]').extract())
        item['body'] = re.sub('<!-- google_ad_section_end -->','',body[65:-6]) # remove div and google tags
        item['bodylen'] = len(item['body'])
        item['timestamp'] = datetime.strptime(response.xpath('//i/text()').re_first(r'Geplaatst op\s*(.*)'),'%b %d, %Y, %I:%M %p')
        item['n54ID'] = response.url.split("/")[-2]
        item['n54URL'] = response.url
        item['parentID'] = response.meta['parentID']

        children = response.xpath('//table[@cellspacing=1]//td[not(contains(.,"\xa0"))]//a/@href').extract()

        yield item

        for child in children:
            request = scrapy.Request(child, callback=self.process_children)
            request.meta['parentID'] = item['n54ID']
            yield request

