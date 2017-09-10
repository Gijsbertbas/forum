# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from forum.models import ForumMessageTestModel
from scrapy.exceptions import DropItem

class ForumPipeline(object):
    def process_item(self, item, spider):

        if ForumMessageTestModel.objects.filter(n54ID=item['n54ID']).exists(): 
        
            raise DropItem("Post already exists %s" % item['n54ID'])

        else:

            if item['parentID']:
                parent = ForumMessageTestModel.objects.get(n54ID=item['parentID'])
                parent.add_child(**item)
            else:
                ForumMessageTestModel.add_root(**item)
            
