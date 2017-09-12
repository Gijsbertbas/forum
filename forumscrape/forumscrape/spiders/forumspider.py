import scrapy
from scrapy.shell import inspect_response
from forumscrape.items import ForumDjangoItem
from datetime import datetime
import os

class ForumLoginSpider(scrapy.Spider):
    name = 'scrapeforum'
    start_urls = ['http://www.network54.com/Forum/95272']

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'username': os.environ['FORUMUSER'], 'password': os.environ['FORUMPASSWORD']},
            callback=self.after_login
        )

    def after_login(self, response):
    
        # add a loop here for all index pages (1:420) when in production
        parents = [] # replace [] with the response.xpath....extract() of the next line 
        parents.append(response.xpath('//table[@cellspacing=1]//td[not(contains(.,"\xa0"))]//a/@href').extract_first())
        parents = response.xpath('//table[@cellspacing=1]//td[not(contains(.,"\xa0"))]//a/@href').extract()
        
        for parent in parents:
            #parent = 'http://www.network54.com/Forum/95272/message/978460501/GastuH'# forcing a specific message for testing
            request = scrapy.Request(parent, callback=self.process_message)
            request.meta['parentID'] = None
            yield request
        
    def process_message(self, response):
        item = ForumDjangoItem()

        item['title'] = response.xpath('//h1/text()').extract_first()
        item['author'] = response.xpath('//h1/following-sibling::text()').re_first(r'by\s([^\(]+)')
        item['body'] = ''.join(response.xpath('//div[@class="intelliTxt KonaBody"]//node()').extract()[1:-1])
        item['timestamp'] = datetime.strptime(response.xpath('//i/text()').re_first(r'Geplaatst op\s*(.*)'),'%b %d, %Y, %I:%M %p')
        item['n54ID'] = response.url.split("/")[-2]
        item['n54URL'] = response.url
        item['parentID'] = response.meta['parentID']
        
        #inspect_response(response, self) # opens terminal
        
        children = response.xpath('//table[@cellspacing=1]//td[not(contains(.,"\xa0"))]//a/@href').extract() 
        # if no children this returns an empty list

        yield item

        for child in children:
            request = scrapy.Request(child, callback=self.process_message)
            request.meta['parentID'] = item['n54ID']
            yield request
            
class ForumMessageSpider(scrapy.Spider):

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

