'''
extracting some facts and figures from the database

run from DJANGO SHELL with:
exec(open("extractfacts.py").read())

this script saves all items as a dictionary in a pickle file.
to be used for graphics later.
'''
from django.db.models import Count, Sum
from forum.models import ForumMessageModel
import pickle
import math
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
    postspauthor = ForumMessageModel.objects.values('author').annotate(
                    count=Count('author'), 
                    totallength=Sum('bodylen'),
                    dead=Count(Case(When(numchild=0, then=1),outputfield=IntegerField()))
                    ).order_by('-count')

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

    postspprins = []
    for prins in prinsennamen:
        temp={}
        posts=0
        length=0
        alldead=0
        for item in postspauthor:
            if item['author'] in prins['pseudoniemen']:
                posts+=item['count']
                length+=item['totallength']
                alldead+=item['dead']
        temp['naam'] = prins['naam']
        temp['posts'] = posts
        temp['averagepostlength'] = length/posts
        temp['percentagedead'] = alldead*100/posts
        postspprins.append(temp)

    return postspauthor[:], postspprins, prinsennamen

def forumperhour():
    perhour=[] # creating a list of dictionaries which can easily be converted to dataframe with pandas.DataFrame.from_dict(perhour).set_index('year')
    for year in range(2001,2015):
        ph={'year':year}
        for hour in range(24):
            ph[hour] = ForumMessageModel.objects.filter(timestamp__year=year).filter(timestamp__hour=hour).count()
        perhour.append(ph)
    return perhour

def forumperweek():
    perweek=[]
    for year in range(2001,2015):
        pw = {'year':year}
        for week in range(1,53):
            pw[week] = ForumMessageModel.objects.filter(timestamp__year=year).filter(timestamp__week=week).count()
        perweek.append(pw)
    return perweek

def forumpickle():
    forumfacts = {}
    forumfacts['totals'] = forumtotals()
    forumfacts['perhour'] = forumperhour()
    forumfacts['perweek'] = forumperweek()
    forumfacts['postsperauthor'], forumfacts['postsperprins'],forumfacts['prinsennamen'] = forumperperson()

    with open('../forumillustrations/forumfacts.pickle', 'wb') as pc:
        pickle.dump(forumfacts,pc)
