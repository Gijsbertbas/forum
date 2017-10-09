from forum.models import ForumMessageModel
import re

gend = ForumMessageModel.objects.get(id=1).body[-36:-6]

for item in ForumMessageModel.objects.all():
    item.body = re.sub(gend,'',item.body[65:-6])
    item.save()
