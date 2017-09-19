'''
extracting some interesting facts and figures from the database

run from within django shell with:
exec(open("data_analysis.py").read())

for inst in ForumMessageModel.objects.all(): inst.author = inst.author.strip(); inst.save()

'''
from django.db.models import Count, Max #,Q
import operator
from forum.models import ForumMessageModel

print('\n TOTALS:')
print('%i baarden' % ForumMessageModel.get_root_nodes().count())
print('%i posts' % ForumMessageModel.objects.all().count())

print('\n TOP 10 POSTERS:')
postsperprins = ForumMessageModel.objects.values('author').annotate(count=Count('author')).order_by('-count')
for item in postsperprins[:10]:
    print('%i posts door %s' % (item['count'], item['author']))

print('\n WORDCOUNT:')
keywords = ['tieten','kut','geil','gast','gasten','bier','pils','brak','PrinsPils','USR']
for key in keywords:
    print('%i posts met het woord \'%s\'' % (ForumMessageModel.objects.filter(body__icontains=key).count(), key)) # 'icontains' should be case insensitive thought I didn't see diff with 'contains'

print('\n PER YEAR:')
for year in range(2001,2015):
    print('%i posts in %i' % (ForumMessageModel.objects.filter(timestamp__year=year).count(), year))

print('\n LONGEST DISCUSSION:')
print('%i posts in de langste discussie' % ForumMessageModel.objects.all().aggregate(Max('depth'))['depth__max'])

print('\n PER HOUR:')
for hour in range(24):
    print('%i posts tussen %i en %i uur' % (ForumMessageModel.objects.filter(timestamp__hour=hour).count(),hour,hour+1))

'''
data=[316,1158,2201,2097,2937,6538,4152,3169,2669,1350,790,75,16,1]
py=pd.Series(data=data,index=pd.PeriodIndex(start=2001,end=2014)

regex for URLs
'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'

import re
match=re.compile(r'(?<=</a>)(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?')
withlink = ForumMessageModel.objects.filter(body__contains="<a href=")
for message in withlink:
    message.body = re.sub(match,'',message.body)
    message.save()

scrapy crawl checkmissingposts -o missing.csv

proefschrift 1303996779

grappige berichten:
http://deprinsen.pythonanywhere.com/forum/message/1019404061 : lycos mail geeft wel 15 MB !! mailbox
http://deprinsen.pythonanywhere.com/forum/message/1142343754 : jc namen suggesties
http://deprinsen.pythonanywhere.com/forum/message/1008843377 : statistieken met in de baard melding dat R en mart te weinig posten
'''
