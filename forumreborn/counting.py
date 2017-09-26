from forum.models import ForumMessageModel
from django.db.models import Count

#print('\n TOP 10 POSTERS:')

postsperprins = ForumMessageModel.objects.values('author').annotate(count=Count('author')).order_by('-count')
#for item in postsperprins[:10]:
#    print('%i posts door %s' % (item['count'], item['author']))

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
    print('%i posts door %s' % (posts, prins['naam']))

'''
['F','Folkert','f','goof','F`','fdboer','folkert','Goof','Goov','gahast!','goov','F de sloperd','gast']
['Roobin','R','r','roobin','ROOBIN','Rooobin','Rwisman','R`','Roobin`','rOOBIN','Robert','roobvin','RRoobin','Roob in','Roobi','Robin','Roobinm','Roobinq','Roobinn','Rooin','@rwisman','RObert','ROobin','Rioobin','Roobin.','Roobion','Roobn','Roobni','Roonin','\roobin','`Roobin','robert','roobi','rrrrrooooooooooooobin','rwi18736','rwisman@gmail.com']
['P','p','DE RUG','douwe','Douwe','De Rug','Pablow','le Locomotive','pb']
['h','Hennie','H','Boogie','Hendrik','hennie','de P.C.','De P.C.','Hennei','de Porno Commissaris','de Porno-Commissaris,'den P.C.','HEnnie','Henny','De Porno Commissaris','boogie','hendrik','De Porno-Commissaris','Henie','Hennnie','Porno Commissaris','de PC','BOOGSIEMEISTER DE COMPUMEISTER','Boogiie','De Porno-Commissars','HEnnei','Hendriquez','Henduhrik','HenniI','Hennie.','Hennied','Hennies','Hennii','Mijnheer de Porno Commissaris','`h','de P.Commissaris','h?','h`']
['koning','Koning','Koningsveld','pk','PK','koningsveld','konign','KOning','konin','pieter koningsveld','KOningsveld','Konignsveld','Koning vanuit zwitserland','Koningsveld jr.','Mevrouw Koningsveld','Vooghel','koning?','koninh','koninkje','pietert k','prinskoni`ng','prinskoning']
['B','bert','Bert','b','gijs','gb','le B','GB','Gijs','Gijsbert','gijsbert','le bert','le b','Bertus','G','le Bert','B.','bertus','glb','leB','bert','Cheis','Gb','Gijbert','Gijs B','Gijsbert bastiaan straathof','don gijs','gbs','gijsb','gis','glijs','lebert','ome bertus']
['A','Kok','VPC','V.P.C.','kok','vpc','A Kok','A. Kok','Vieze P.C.','a','Hein','v.p.c.','A.Kok','Alfons','De A is van Andre dus gewoon Kok','De vieze P.C.','Hendricus Alphonsus Cornelis Kok','KOK','Koksy','V.P.C','de V.P.C.','de Vieze Porno commissaris']
['W','Wildeman','w','wildeman','Henkie','Pieter W','P~W','W`','`W','henkie','pw']
['pp','PP']
['mart','Mart','MArt','M','m','MART','Marty pooper','Marrrrrrrt','Martuary','harryhardcore','mART','MART the anonymous','M^art','Mart de econoom','Mart goes vietnam','Mrt','Mrtr','Prins MArt','Prins Mart','mart de enterpeneur','marto','marty','martyparty','sMART']
'''