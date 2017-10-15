# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from forum.models import ForumMessageModel

class ForumMissingItem(scrapy.Item):

    indexpage = scrapy.Field()
    postids = scrapy.Field()

class ForumDjangoItem(DjangoItem):

    django_model = ForumMessageModel

    def __repr__(self):
        """only print out attr1 after exiting the Pipeline"""
        return repr("scraped another post")
