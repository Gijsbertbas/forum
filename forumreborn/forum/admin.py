from django.contrib import admin

# Register your models here.
from .models import ForumMessageTestModel

class ForumMessagesAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = ('id','timestamp','author','title','n54ID','n54URL')


admin.site.register(ForumMessageTestModel, ForumMessagesAdmin)

