'''
extracting some interesting facts and figures from the database

run from within django shell with:
exec(open("./data_analysis.py").read())

for inst in ForumMessageModel.objects.all(): inst.author = inst.author.strip(); inst.save()

'''
from django.db.models import Count, Max #,Q
import operator
from forum.models import ForumMessageModel

print('\n TOTALS:')
print('%i baarden' % ForumMessageModel.get_root_nodes().count())
print('%i posts' % ForumMessageModel.objects.all().count())

postsperprins = ForumMessageModel.objects.values('author').order_by('author').annotate(count=Count('author'))
postsperprins = list(postsperprins)
postsperprinsdict = {}
for item in postsperprins:
    postsperprinsdict[item['author'].strip()] = item['count']

topposters = sorted(postsperprinsdict.items(), key=operator.itemgetter(1), reverse=True)
print('\n TOP 10 POSTERS:')
for name, count in topposters[:10]:
    print('%i posts door %s' % (count, name))

print('\n WORDCOUNT:')
keywords = ['tieten','kut','geil','gast','gasten','bier','pils','brak','PrinsPils','USR']
for key in keywords:
    print('%i posts met het woord \'%s\'' % (ForumMessageModel.objects.filter(body__icontains=key).count(), key)) # 'icontains' should be case insensitive thought I didn't see diff with 'contains'

print('\n PER YEAR:')
for year in range(2001,2015):
    print('%i posts in %i' % (ForumMessageModel.objects.filter(timestamp__year=year).count(), year))

print('\n LONGEST DISCUSSION:')
print('%i posts in de langste discussie' % ForumMessageModel.objects.all().aggregate(Max('depth'))['depth__max'])
