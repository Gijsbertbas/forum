from django.db import models
from treebeard.mp_tree import MP_Node

class ForumMessageTestModel(MP_Node):

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    body = models.TextField()
    timestamp = models.DateTimeField()
    n54ID = models.IntegerField()
    n54URL = models.URLField(max_length=200)
    parentID = models.IntegerField(null=True)

    node_order_by = ['timestamp']

class TestModel(MP_Node):

    title = models.CharField(max_length=200)
    parentID = models.IntegerField(null=True)


'''
    def __unicode__(self):
        return 'Network54 ID: %d' % self.n54ID

from treebeard_tutorial.models import Category
get = lambda node_id: Category.objects.get(pk=node_id)
root = Category.add_root(name='Computer Hardware')
node = get(root.pk).add_child(name='Memory')
get(node.pk).add_sibling(name='Hard Drives')
<Category: Category: Hard Drives>
get(node.pk).add_sibling(name='SSD')
<Category: Category: SSD>
get(node.pk).add_child(name='Desktop Memory')
<Category: Category: Desktop Memory>
get(node.pk).add_child(name='Laptop Memory')
<Category: Category: Laptop Memory>
get(node.pk).add_child(name='Server Memory')
<Category: Category: Server Memory>
'''


