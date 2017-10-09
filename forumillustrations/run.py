import re
from wordcloud import WordCloud
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import random
import pandas as pd
import pickle

# FOR WORDCLOUD
# ideas: orange instead of grey, vector format output?, test size and number of words
def postswordcloud(reload=False):

    def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return "hsl(30, %d%%, 50%%)" % random.randint(60, 100)

    if reload:
        from forum.models import ForumMessageModel
        output = open('posts.dat','a')
        for post in ForumMessageModel.objects.all():
            output.write(post.body[65:-36])
        output.close()

        text = open('posts.dat').read()
        text = re.sub('<([^<>]+)>','',text)
        text = re.sub('\n','',text)
        with open('posts.dat','w') as output:
            output.write(text)
    else:
        text = open('posts.dat').read()
        
    stops = set(open('stopwords.txt').read().splitlines())
    mask = np.array(Image.open('utrecht_mask.png'))
    
    wc = WordCloud( background_color="white", 
                    max_words=2000, 
                    mask=mask, 
                    stopwords=stops,
                    max_font_size=40,
                    scale=20
                    )
    wc.generate(text)
    wc.recolor(color_func=grey_color_func, random_state=3)
    wc.to_file('forumwordcloud.png')


def loadpickle():
    return pickle.load(open('forumfacts.pickle','rb')) 

def recolorplot(ax, color='#FF9900'):
    ax.spines['bottom'].set_color(color)
    ax.spines['top'].set_color(color)
    ax.spines['right'].set_color(color)
    ax.spines['left'].set_color(color)
    ax.tick_params(axis='x', colors=color)
    ax.tick_params(axis='y', colors=color)
    ax.yaxis.label.set_color(color)
    ax.xaxis.label.set_color(color)
    ax.title.set_color(color)


def forumperweek():
    perweek = loadpickle()['perweek']

    ax = perweek.sum(axis=1).plot.line(lw=3,c='#FF9900')
    plt.xticks(np.arange(3,50,4),['jan','feb','mrt','apr','mei','jun','jul','aug','sep','okt','nov','dec'])
    plt.ylim([0,1.1*perweek.sum(axis=1).max()])
    recolorplot(ax,color='#FF9900')
    plt.savefig('perweek.png')
    plt.close()
    
def forumperhour():
    perhour = loadpickle()['perhour']

    ax = perhour.sum(axis=1).plot.line(lw=3,c='#FF9900')
    plt.ylim([0,1.1*perhour.sum(axis=1).max()])
    plt.xlabel('uur'); plt.ylabel('posts')
    plt.title('posts door de dag')
    recolorplot(ax,color='#FF9900')
    plt.savefig('perhour.svg')
    plt.close()
    
    for column in perhour.columns:
        perhour.loc[:,column] = perhour.loc[:,column]/perhour.loc[:,column].max()

    plt.figure()
    plt.imshow(perhour, interpolation='spline16', aspect='auto', cmap='Wistia', origin='lower')
    plt.yticks(np.arange(0,len(perhour.index),1),perhour.index)
    plt.xticks(np.arange(0,len(perhour.columns),1),perhour.columns)
    plt.savefig('perhourmap.png')
    plt.close()

def forumhistogram():
    ppp = loadpickle()['postsperprins']
    ppp.reverse()

    ds = pd.Series()
    for p in ppp:
        ds[p[0]] = p[1]

    ax = ds.plot.barh(color='#FF9900')
    recolorplot(ax)
    plt.xlim([0,7700])
    plt.savefig('posthistogram.svg')
    plt.close()

    ppa = loadpickle()['postsperauthor']
    ppa.reverse()

    ds = pd.Series()
    for a in ppa[-20:]:
        ds[a['author']] = a['count']

    plt.figure()
    ax = ds.plot.barh(color='#FF9900')
    recolorplot(ax)
    plt.xlim([0,7700])
    plt.savefig('posthistograma.svg')
    plt.close()

'''
    plt.axis('off')

for prins in prinsennamen:
    for ps in prins['pseudoniemen']:
        try:
            posterslist.remove(ps)
        except:
            print('not in')

'''
