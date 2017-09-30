'''
extracting some interesting facts and figures from the database

run from within django shell with:
exec(open("data_analysis.py").read())

'''
from django.db.models import Count, Max #,Q
from forum.models import ForumMessageModel
import operator

print('\n TOTALS:')
baarden = ForumMessageModel.get_root_nodes().count()
print('%i baarden (%i index paginas)' % (baarden, baarden/20))
posts = ForumMessageModel.objects.all().count()
missing = (421*20-baarden)*posts/baarden
ids = open('missing.dat').read().split(',')
ids_seen = ForumMessageModel.objects.all().values_list('n54ID',flat=True)
_ = [ids.remove(str(x)) for x in ids_seen if str(x) in ids]
print('%i posts (%i to go...)' % (posts,len(ids)))

print('\n TOP 10 POSTERS:')
postsperprins = ForumMessageModel.objects.values('author').annotate(count=Count('author')).order_by('-count')
for item in postsperprins[:10]:
    print('%i posts door %s' % (item['count'], item['author']))
print('\n .. en nu inclusief alle pseudoniemen...')
prinsennamen = [];
prinsennamen.append({'naam': 'Gast', 'pseudoniemen': ['F','Folkert','f','goof','F`','fdboer','folkert','Goof','Goov','gahast!','goov','F de sloperd','gast']})
prinsennamen.append({'naam': 'Roobin','pseudoniemen': ['Roobin','R','r','roobin','ROOBIN','Rooobin','Rwisman','R`','Roobin`','rOOBIN','Robert','roobvin','RRoobin','Roob in','Roobi','Robin','Roobinm','Roobinq','Roobinn','Rooin','@rwisman','RObert','ROobin','Rioobin','Roobin.','Roobion','Roobn','Roobni','Roonin','\roobin','`Roobin','robert','roobi','rrrrrooooooooooooobin','rwi18736','rwisman@gmail.com']})
prinsennamen.append({'naam': 'Boogie', 'pseudoniemen': ['h','Hennie','H','Boogie','Hendrik','hennie','de P.C.','De P.C.','Hennei','de Porno Commissaris','de Porno-Commissaris','den P.C.','HEnnie','Henny','De Porno Commissaris','boogie','hendrik','De Porno-Commissaris','Henie','Hennnie','Porno Commissaris','de PC','BOOGSIEMEISTER DE COMPUMEISTER','Boogiie','De Porno-Commissars','HEnnei','Hendriquez','Henduhrik','HenniI','Hennie.','Hennied','Hennies','Hennii','Mijnheer de Porno Commissaris','`h','de P.Commissaris','h?','h`']})
prinsennamen.append({'naam': 'P', 'pseudoniemen': ['P','p','DE RUG','douwe','Douwe','De Rug','Pablow','le Locomotive','pb']})
prinsennamen.append({'naam': 'Koning', 'pseudoniemen': ['koning','Koning','Koningsveld','pk','PK','koningsveld','konign','KOning','konin','pieter koningsveld','KOningsveld','Konignsveld','Koning vanuit zwitserland','Koningsveld jr.','Mevrouw Koningsveld','Vooghel','koning?','koninh','koninkje','pietert k','prinskoni`ng','prinskoning']})
prinsennamen.append({'naam': 'PP', 'pseudoniemen': ['pp','PP']})
prinsennamen.append({'naam': 'Wildeman', 'pseudoniemen': ['W','Wildeman','w','wildeman','Henkie','Pieter W','P~W','W`','`W','henkie','pw']})
prinsennamen.append({'naam': 'Kok', 'pseudoniemen': ['A','Kok','VPC','V.P.C.','kok','vpc','A Kok','A. Kok','Vieze P.C.','a','Hein','v.p.c.','A.Kok','Alfons','De A is van Andre dus gewoon Kok','De vieze P.C.','Hendricus Alphonsus Cornelis Kok','KOK','Koksy','V.P.C','de V.P.C.','de Vieze Porno commissaris']})
prinsennamen.append({'naam': 'Bertus', 'pseudoniemen': ['B','bert','Bert','b','gijs','gb','le B','GB','Gijs','Gijsbert','gijsbert','le bert','le b','Bertus','G','le Bert','B.','bertus','glb','leB','bert','Cheis','Gb','Gijbert','Gijs B','Gijsbert bastiaan straathof','don gijs','gbs','gijsb','gis','glijs','lebert','ome bertus']})
prinsennamen.append({'naam': 'Mart', 'pseudoniemen': ['mart','Mart','MArt','M','m','MART','Marty pooper','Marrrrrrrt','Martuary','harryhardcore','mART','MART the anonymous','M^art','Mart de econoom','Mart goes vietnam','Mrt','Mrtr','Prins MArt','Prins Mart','mart de enterpeneur','marto','marty','martyparty','sMART']})

postspp = {}
for prins in prinsennamen:
    posts=0
    for item in postsperprins:
        if item['author'] in prins['pseudoniemen']:
            posts+=item['count']
    postspp[prins['naam']] = posts
postspp_sorted = sorted(postspp.items(), key=operator.itemgetter(1), reverse=True)
_=[print('%i posts door %s'%(i[1],i[0])) for i in postspp_sorted]

print('\n WORDCOUNT:')
keywords = ['tieten','kut','geil','gast','gasten','bier','pils','brak','PrinsPils','USR']
for key in keywords:
    print('%i posts met het woord \'%s\'' % (ForumMessageModel.objects.filter(body__icontains=key).count(), key)) # 'icontains' should be case insensitive thought I didn't see diff with 'contains'

print('\n PER YEAR:')
for year in range(2001,2015):
    print('%i posts in %i' % (ForumMessageModel.objects.filter(timestamp__year=year).count(), year))

print('\n LONGEST DISCUSSION:')
maxdepth = ForumMessageModel.objects.all().aggregate(Max('depth'))['depth__max']
print('%i posts in de langste discussie' % maxdepth)
print('posted on %s' % ForumMessageModel.get_root(ForumMessageModel.objects.filter(depth=maxdepth)[0]).timestamp) #could be more than 1

'''
print('\n PER HOUR:')
for hour in range(24):
    print('%i posts tussen %i en %i uur' % (ForumMessageModel.objects.filter(timestamp__hour=hour).count(),hour,hour+1))

ERRORS:
table issues example: proefschrift 1303996779
repeated text: 1145277452

PANDAS:
import pandas as pd
perhour=pd.DataFrame(index=pd.PeriodIndex(start=0, end=23)
for year in range(2001,2015):
    for hour in range(24):
        perhour[hour][year]=ForumMessageModel.objects.filter(timestamp__year=year).filter(timestamp__hour=hour).count()

data=[316,1158,2201,2097,2937,6538,4152,3169,2669,1350,790,75,16,1]
py=pd.Series(data=data,index=pd.PeriodIndex(start=2001,end=2014)

CORRECT POSTS WITH LINK:
regex for URLs
seems to work: '(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'
alternative: 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

import re
match=re.compile(r'(?<=</a>)(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?')
withlink = ForumMessageModel.objects.filter(body__contains="<a href=")
for message in withlink:
    message.body = re.sub(match,'',message.body)
    message.save()

CHECK MISSING POSTS:
! cancel pipeline !
scrapy crawl checkmissingposts -t csv -o missing.csv --loglevel=INFO

GRAPPIG:
1032350845
http://deprinsen.pythonanywhere.com/forum/message/1019404061 : lycos mail geeft wel 15 MB !! mailbox
http://deprinsen.pythonanywhere.com/forum/message/1142343754 : jc namen suggesties
http://deprinsen.pythonanywhere.com/forum/message/1008843377 : statistieken met in de baard melding dat R en mart te weinig posten
http://deprinsen.pythonanywhere.com/forum/message/980431599 : boogie en folkert (goof!) verdedigen Mart
'''
