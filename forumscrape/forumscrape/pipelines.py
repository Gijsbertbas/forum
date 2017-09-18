# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from forum.models import ForumMessageModel
from scrapy.exceptions import DropItem

class ForumPipeline(object):

    def process_item(self, item, spider):

        if ForumMessageModel.objects.filter(n54ID=item['n54ID']).exists(): 
        
            raise DropItem("Post %s already exists..." % item['n54ID'])

        else:

            if item['parentID']:
                parent = ForumMessageModel.objects.get(n54ID=item['parentID'])
                parent.add_child(**item)
            else:
                ForumMessageModel.add_root(**item)
            
class ForumPipelineInfill(object):
    def __init__(self):
        self.ids_seen = ForumMessageModel.objects.all().values_list('n54ID',flat=True)

    def process_item(self, item, spider):

        if item['n54ID'] in self.ids_seen: 
        
            raise DropItem("Post %s already exists..." % item['n54ID'])

        else:
        
            if item['parentID']:
                parent = ForumMessageModel.objects.get(n54ID=item['parentID'])
                parent.add_child(**item)
            else:
                ForumMessageModel.add_root(**item)

