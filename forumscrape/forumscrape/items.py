# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from forum.models import ForumMessageModel


class ForumMessageItem(scrapy.Item):
    
    title = scrapy.Field()
    author = scrapy.Field()
    body = scrapy.Field()
    timestamp = scrapy.Field()
    n54ID = scrapy.Field()
    n54URL = scrapy.Field()
    hasparent = scrapy.Field()
    parentID = scrapy.Field()
    
class ForumDjangoItem(DjangoItem):

    django_model = ForumMessageModel

    def __repr__(self):
        """only print out attr1 after exiting the Pipeline"""
        return repr("scraped another item")
