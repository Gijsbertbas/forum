from forum.models import ForumMessageModel
from django.db.models import Count

#print('\n TOP 10 POSTERS:')

postsperprins = ForumMessageModel.objects.values('author').annotate(count=Count('author')).order_by('-count')
#for item in postsperprins[:10]:
#    print('%i posts door %s' % (item['count'], item['author']))

prinsennamen = [];
prinsennamen.append({'naam': 'Gast', 'pseudoniemen': ['F','f','Goof','goof','Folkert','folkert']})
prinsennamen.append({'naam': 'Roobin','pseudoniemen': ['Roobin','roobin','R','r','Robert','robert']})
prinsennamen.append({'naam': 'Boogie', 'pseudoniemen': ['Hennie','H','Boogie','Hendrik','h']})
prinsennamen.append({'naam': 'P', 'pseudoniemen': ['P','Douwe','p']})
prinsennamen.append({'naam': 'Koning', 'pseudoniemen': ['Koning','koning']})
prinsennamen.append({'naam': 'PP', 'pseudoniemen': ['PP','pp']})
prinsennamen.append({'naam': 'Wildeman', 'pseudoniemen': ['W','w','Wildeman']})
prinsennamen.append({'naam': 'Kok', 'pseudoniemen': ['A','alphons','Kok','kok','VPC']})
prinsennamen.append({'naam': 'Bertus', 'pseudoniemen': ['B','bertus','b','Gijs']})
prinsennamen.append({'naam': 'Mart', 'pseudoniemen': ['Mart','mart']})

postspp = {}
for prins in prinsennamen:
    posts=0
    for item in postsperprins:
        if item['author'] in prins['pseudoniemen']:
            posts+=item['count']
    postspp[prins['naam']] = posts

'''
'F','Folkert',
'Roobin','R','r','roobin',
'P','p',
'h','Hennie','H','Boogie','Hendrik','hennie',
'koning','Koning','Koningsveld',
'B','bert','Bert','b','gijs','gb','le B','GB','Gijs',
'A','Kok','VPC','V.P.C.',
'W','Wildeman',
'pp','PP',
'mart','Mart','MArt','M','m',

'f'
'de P.C.'
'Gijsbert'
'gijsbert'
'pk'
'PK'
'koningsveld'
'le bert'
'MART'
'kok'
'ROOBIN'
'Rooobin'
'le b'
'Bertus'
'De P.C.'
'G'
'Rwisman'
'goof'
'le Bert'
'DE RUG','douwe','Douwe'
'w','wildeman'
'R`'



,'Roobin`','rOOBIN'
F`
Hennei
Robert
de Porno Commissaris
de Porno-Commissaris
den P.C.
fdboer
folkert
roobvin
vpc
A Kok
Goof
HEnnie
Henny
RRoobin
Roob in
Roobi
konign
A. Kok
B.
De Porno Commissaris
KOning
Marty pooper
Pieter
Robin
Roobinm
Roobinq
Vieze P.C.
a
boogie
hendrik
De Porno-Commissaris
Goov
Hein
Henie
Hennnie
Marrrrrrrt
Martuary
Porno Commissaris
Roobinn
Rooin
bertus
de PC
gahast!
glb
goov
harryhardcore
konin
leB
mART
pieter koningsveld
v.p.c.
'bert
@rwisman
A.Kok
Alfons
BOOGSIEMEISTER DE COMPUMEISTER
Boogiie
Cheis
De A is van Andre dus gewoon Kok
De Porno-Commissars
De Rug
De vieze P.C.
F de sloperd
Gb
Gijbert
Gijs B
Gijsbert bastiaan straathof
HEnnei
Hendricus Alphonsus Cornelis Kok
Hendriquez
Henduhrik
Henkie
HenniI
Hennie.
Hennied
Hennies
Hennii
K
KOK
KOningsveld
Koksy
Konignsveld
Koning vanuit zwitserland
Koningsveld jr.
MART the anonymous
M^art
Mart de econoom
Mart goes vietnam
Mevrouw Koningsveld
Mijnheer de Porno Commissaris
Mrt
Mrtr
PP-DC
Pablow
Pieter W
Prins MArt
Prins Mart
P~W
RObert
ROobin
Rioobin
Roobin.
Roobion
Roobn
Roobni
Roonin
V.P.C
Vooghel
W`
\roobin
`Roobin','robert','roobi','rrrrrooooooooooooobin','rwi18736','rwisman@gmail.com'
'`W
'`h
'de P.Commissaris
'de V.P.C.
'de Vieze Porno commissaris
'don gijs
'gast
'gbs','gijsb','gis','glijs','lebert','ome bertus'
'h?','h`'
henkie

'koning?
'koninh
'koninkje

'le Locomotive

'mart de enterpeneur
'marto
'marty
'martyparty

pb
pietert k
prinskoni`ng
prinskoning
pw

'sMART
'''