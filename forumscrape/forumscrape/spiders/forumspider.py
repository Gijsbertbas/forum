import scrapy
from scrapy.shell import inspect_response
from forumscrape.items import ForumDjangoItem
from datetime import datetime

class ForumLoginSpider(scrapy.Spider):
    name = 'scrapeforum'
    start_urls = ['http://www.network54.com/Forum/95272']

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'prinshennie', 'password': 'hans2206'},
            callback=self.after_login
        )

    def after_login(self, response):
    
        # add a loop here for all index pages (1:420) when in production
        parents = [] # replace [] with the response.xpath....extract() of the next line 
        parents.append(response.xpath('//table[@cellspacing=1]//td[not(contains(.,"\xa0"))]//a/@href').extract_first())
        
        for parent in parents:
            parent = 'http://www.network54.com/Forum/95272/message/978460501/GastuH'# forcing a specific message for testing
            request = scrapy.Request(parent, callback=self.process_message)
            request.meta['parentID'] = None
            yield request
        
    def process_message(self, response):
        item = ForumDjangoItem()

        item['title'] = response.xpath('//h1/text()').extract_first()
        item['author'] = response.xpath('//h1/following-sibling::text()').re_first(r'by\s([^\(\s]+)')
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
            
'''
some code dump:

produces a list of all links for 'parent' posts (apparently '&nbsp;' is translated to '\xa0')
list=response.xpath('//table[@cellspacing=1]//td[not(contains(.,"\xa0"))]//a/@href').extract()

        item['title'] = response.xpath('//h1/text()').extract_first()
        item['author'] = response.xpath('//h1/following-sibling::text()').re_first(r'by\s([^\(\s]+)')
        item['body'] = ''.join(response.xpath('//div[@class="intelliTxt KonaBody"]//node()').extract()[1:-1])
        item['date'] = datetime.strptime(response.xpath('//i/text()').re_first(r'Geplaatst op\s*(.*)'),'%b %d, %Y, %I:%M %p')
        item['network54ID'] = response.url.split("/")[-2]
        item['network54URL'] = response.url
        item['hasparent'] = False
        item['parent'] = parent


'''

class ForumSpider(scrapy.Spider):
    name = "forum"
    start_urls =[
        'http://www.network54.com/forum/95272/',
    ]
    
    def parse(self,response):
        page = response.url.split("/")[-2]
        filename = 'forum/quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)

