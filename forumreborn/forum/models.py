from django.db import models
from treebeard.mp_tree import MP_Node

class ForumMessageModel(MP_Node):

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    body = models.TextField()
    timestamp = models.DateTimeField()
    n54ID = models.IntegerField()
    n54URL = models.URLField(max_length=200)
    parentID = models.IntegerField(null=True)

    node_order_by = ['timestamp']

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


