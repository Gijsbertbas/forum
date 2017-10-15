import re
from wordcloud import WordCloud
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import random
import pandas as pd
import pickle

def forumwordcloud():

    def orange_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return "hsl(30, %d%%, 50%%)" % random.randint(60, 100) # forum orange #FF9900; HSL 36,100,50

    def orange_white_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return "hsl(36, 100%%, %d%%)" % random.randint(80, 100) # forum orange #FF9900; HSL 36,100,50

    text = open('posts.dat').read()
    stops = set(open('stopwords.txt').read().splitlines())
    mask = np.array(Image.open('utrecht_mask.png'))
    
    wc = WordCloud( background_color='white', 
                    max_words=2000, 
                    mask=mask, 
                    stopwords=stops,
                    max_font_size=40,
                    scale=3,
                    mode='RGBA',
                    alpha=0
                    )
    wc.generate(text)
    wc.recolor(color_func=orange_white_color_func, random_state=3)
    wc.to_file('forumwordcloud.png')


def loadpickle(dict):
    return pickle.load(open('forumfacts.pickle','rb'))[dict]

def recolorlineplot(ax, color='#FF9900'):
    ax.spines['bottom'].set_color(color)
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color(color)
    ax.tick_params(axis='x', colors=color)
    ax.tick_params(axis='y', colors=color)
    ax.yaxis.label.set_color(color)
    ax.xaxis.label.set_color(color)
    ax.title.set_color(color)

def recolorhist(ax, color='#FF9900'):
    ax.spines['bottom'].set_color('none')
    ax.spines['top'].set_color(color)
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.tick_params(axis='x', colors=color)
    ax.tick_params(axis='y', colors=color)
    ax.yaxis.label.set_color(color)
    ax.xaxis.label.set_color(color)
    ax.title.set_color(color)

def recolormap(ax, color='#FF9900'):
    ax.spines['bottom'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.tick_params(axis='x', colors=color)
    ax.tick_params(axis='y', colors=color)
    ax.yaxis.label.set_color(color)
    ax.xaxis.label.set_color(color)
    ax.title.set_color(color)

def forumperweek():
    perweek = loadpickle('perweek')

    fig = plt.figure(figsize=(10,7.5))
    ax = perweek.sum(axis=1).plot.line(lw=3,c='white')
    plt.xticks(np.arange(4,50,4),['jan','feb','mrt','apr','mei','jun','jul','aug','sep','okt','nov','dec'])
    plt.ylim([0,1.1*perweek.sum(axis=1).max()])
    plt.title('alle posts per week')
    recolorlineplot(ax,color='white')
    plt.savefig('perweek.svg', dpi=150, transparent=True, bbox_inches='tight')
    plt.close()
    
def forumperhour():
    perhour = loadpickle('perhour')

    fig1 = plt.figure(figsize=(10,7.5))
    ax1 = perhour.sum(axis=1).plot.line(lw=3,c='white')
    plt.ylim([0,1.1*perhour.sum(axis=1).max()])
    plt.xlabel('uur')
    plt.title('alle posts per tijdstip')
    recolorlineplot(ax1,color='white')
    plt.savefig('perhour.svg', dpi=150, transparent=True, bbox_inches='tight')
    plt.close()
    
    for column in perhour.columns:
        perhour.loc[:,column] = perhour.loc[:,column]/perhour.loc[:,column].max()

    fig2 = plt.figure(figsize=(10,7.5))
    plt.imshow(perhour, interpolation='spline16', aspect='auto', cmap='Wistia', origin='lower')
    plt.xticks(np.arange(0,len(perhour.columns),1),perhour.columns)
    plt.yticks(np.arange(-0.5,24,1),range(25))
    ax2 = plt.gca()
    recolormap(ax2,'white')
    plt.title('heatmap van posts door de dag over de jaren')
    plt.savefig('perhourmap.png', dpi=150, transparent=True, bbox_inches='tight')
    plt.close()

def forumhistogram():
    ppp = loadpickle('postsperprins')
    ppp.reverse()

    ds = pd.Series()
    for p in ppp:
        ds[p[0]] = p[1]

    fig = plt.figure(figsize=(10,7.5))
    ax = ds.plot.barh(color='white')
    total = loadpickle('totals')['posts']
    for p in ax.patches:
        ax.annotate('%i%%' % int(p.get_width()*100/total), (50, p.get_y() + .18), color='#FF9900')
    recolorhist(ax, color='white')
    plt.xlim([0,8000])
    plt.xlabel('Totaal aantal posts per prins')
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    fig.subplots_adjust(left=.15)
    plt.savefig('posthistogram.svg', dpi=150, transparent=True, bbox_inches='tight')
    plt.close()

    ppa = loadpickle('postsperauthor')
    ppa.reverse()

    ds = pd.Series()
    for a in ppa[-20:]:
        ds[a['author']] = a['count']

    fig = plt.figure(figsize=(10,7.5))
    ax = ds.plot.barh(color='white')
    recolorhist(ax, color='white')
    plt.xlim([0,8000])
    plt.xlabel('aantal posts voor de top 20 posters')
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    fig.subplots_adjust(left=.15)
    plt.savefig('posthisttop20.svg', dpi=150, transparent=True, bbox_inches='tight')
    plt.close()
