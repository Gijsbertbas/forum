'''
extracting some interesting facts and figures from the database

run from within django shell with:
exec(open("extractfacts.py").read())

This script saves all items as a dictionary in a pickle file.
To be used for graphics later.
'''
from django.db.models import Count, Max #,Q
from forum.models import ForumMessageModel
import operator
import pickle
import math
import pandas as pd
import re

def forumpoststofile():
    output = open('../forumillustrations/posts.dat','a')
    for post in ForumMessageModel.objects.all():
        output.write(post.body)
    output.close()

    # remove all html tags and end-of-line statements
    text = open('../forumillustrations/posts.dat').read()
    text = re.sub('<([^<>]+)>','',text)
    text = re.sub('\n','',text)
    with open('../forumillustrations/posts.dat','w') as output:
        output.write(text)


# TOTALS:
def forumtotals():
    totals = {}
    totals['baarden'] = ForumMessageModel.get_root_nodes().count()
    totals['indexs'] = math.ceil(totals['baarden']/20)
    totals['posts'] = ForumMessageModel.objects.all().count()
    return totals

# TOP 10 POSTERS:
def forumperperson():
    postspauthor = ForumMessageModel.objects.values('author').annotate(count=Count('author')).order_by('-count')

    prinsennamen = []
    prinsennamen.append({'naam': 'F', 'pseudoniemen': ['F','Folkert','f','goof','F`','fdboer','folkert','Goof','Goov','gahast!','goov','F de sloperd','gast']})
    prinsennamen.append({'naam': 'Roobin','pseudoniemen': ['Roobin','R','r','roobin','ROOBIN','Rooobin','Rwisman','R`','Roobin`','rOOBIN','Robert','roobvin','RRoobin','Roob in','Roobi','Robin','Roobinm','Roobinq','Roobinn','Rooin','@rwisman','RObert','ROobin','Rioobin','Roobin.','Roobion','Roobn','Roobni','Roonin','\roobin','`Roobin','robert','roobi','rrrrrooooooooooooobin','rwi18736','rwisman@gmail.com']})
    prinsennamen.append({'naam': 'h', 'pseudoniemen': ['h','Hennie','H','Boogie','Hendrik','hennie','de P.C.','De P.C.','Hennei','de Porno Commissaris','de Porno-Commissaris','den P.C.','HEnnie','Henny','De Porno Commissaris','boogie','hendrik','De Porno-Commissaris','Henie','Hennnie','Porno Commissaris','de PC','BOOGSIEMEISTER DE COMPUMEISTER','Boogiie','De Porno-Commissars','HEnnei','Hendriquez','Henduhrik','HenniI','Hennie.','Hennied','Hennies','Hennii','Mijnheer de Porno Commissaris','`h','de P.Commissaris','h?','h`']})
    prinsennamen.append({'naam': 'P', 'pseudoniemen': ['P','p','DE RUG','douwe','Douwe','De Rug','Pablow','le Locomotive','pb']})
    prinsennamen.append({'naam': 'koning', 'pseudoniemen': ['koning','Koning','Koningsveld','pk','PK','koningsveld','konign','KOning','konin','pieter koningsveld','KOningsveld','Konignsveld','Koning vanuit zwitserland','Koningsveld jr.','Mevrouw Koningsveld','Vooghel','koning?','koninh','koninkje','pietert k','prinskoni`ng','prinskoning']})
    prinsennamen.append({'naam': 'pp', 'pseudoniemen': ['pp','PP']})
    prinsennamen.append({'naam': 'W', 'pseudoniemen': ['W','Wildeman','w','wildeman','Henkie','Pieter W','P~W','W`','`W','henkie','pw']})
    prinsennamen.append({'naam': 'A', 'pseudoniemen': ['A','Kok','VPC','V.P.C.','kok','vpc','A Kok','A. Kok','Vieze P.C.','a','Hein','v.p.c.','A.Kok','Alfons','De A is van Andre dus gewoon Kok','De vieze P.C.','Hendricus Alphonsus Cornelis Kok','KOK','Koksy','V.P.C','de V.P.C.','de Vieze Porno commissaris']})
    prinsennamen.append({'naam': 'B', 'pseudoniemen': ['B','bert','Bert','b','gijs','gb','le B','GB','Gijs','Gijsbert','gijsbert','le bert','le b','Bertus','G','le Bert','B.','bertus','glb','leB','bert','Cheis','Gb','Gijbert','Gijs B','Gijsbert bastiaan straathof','don gijs','gbs','gijsb','gis','glijs','lebert','ome bertus']})
    prinsennamen.append({'naam': 'mart', 'pseudoniemen': ['mart','Mart','MArt','M','m','MART','Marty pooper','Marrrrrrrt','Martuary','harryhardcore','mART','MART the anonymous','M^art','Mart de econoom','Mart goes vietnam','Mrt','Mrtr','Prins MArt','Prins Mart','mart de enterpeneur','marto','marty','martyparty','sMART']})

    postspprins = {}
    for prins in prinsennamen:
        posts=0
        for item in postspauthor:
            if item['author'] in prins['pseudoniemen']:
                posts+=item['count']
        postspprins[prins['naam']] = posts
    postspprins = sorted(postspprins.items(), key=operator.itemgetter(1), reverse=True)
    
    return postspauthor[:], postspprins, prinsennamen

def forumperhour():
    perhour=pd.DataFrame(index=range(24))
    for year in range(2001,2015):
        posts = []
        for hour in range(24):
            posts.append(ForumMessageModel.objects.filter(timestamp__year=year).filter(timestamp__hour=hour).count())
        perhour[str(year)]=posts
    return perhour
    
def forumperweek():
    perweek=pd.DataFrame(index=range(1,53))
    for year in range(2001,2015):
        posts = []
        for week in range(1,53):
            posts.append(ForumMessageModel.objects.filter(timestamp__year=year).filter(timestamp__week=week).count())
        perweek[str(year)]=posts
    return perweek
    
def forumpickle():
    forumfacts = {}
    forumfacts['totals'] = forumtotals()
    forumfacts['perhour'] = forumperhour()
    forumfacts['perweek'] = forumperweek()
    forumfacts['postsperauthor'], forumfacts['postsperprins'],forumfacts['prinsennamen'] = forumperperson()

    with open('forum/static/forum/forumfacts.pickle', 'wb') as pc:
        pickle.dump(forumfacts,pc)

'''
REGEX FOR URLS
seems to work: '(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'
alternative: 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

GRAPPIG:
1032350845
1019404061 : lycos mail geeft wel 15 MB !! mailbox
1142343754 : jc namen suggesties
1008843377 : statistieken met in de baard melding dat R en mart te weinig posten
980431599 : boogie en folkert (goof!) verdedigen Mart
1065687101 : gratis internet bij de mediamarkt 2003
'''
