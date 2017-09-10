# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from forum.models import ForumMessageTestModel

class ForumPipeline(object):
    def process_item(self, item, spider):

        if item['parentID']:
            parent = ForumMessageTestModel.objects.get(n54ID=item['parentID'])
            parent.add_child(**item)
        else:
            ForumMessageTestModel.add_root(**item)
            
        #return item


