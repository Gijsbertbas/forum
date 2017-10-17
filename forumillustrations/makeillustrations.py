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
    pw = loadpickle('perweek')
    perweek = pd.DataFrame.from_dict(pw).set_index('year')

    plt.figure(figsize=(10,7.5))
    ax = perweek.sum(axis=0).plot.line(lw=3,c='white')
    plt.xticks(np.arange(4,50,4),['jan','feb','mrt','apr','mei','jun','jul','aug','sep','okt','nov','dec'])
    plt.ylim([0,1.1*perweek.sum(axis=0).max()])
    plt.title('posts door het jaar')
    recolorlineplot(ax,color='white')
    plt.savefig('perweek.svg', dpi=150, transparent=True, bbox_inches='tight')
    plt.close()

def forumperhour():
    ph = loadpickle('perhour')
    perhour = pd.DataFrame.from_dict(ph).set_index('year')

    fig1 = plt.figure(figsize=(10,7.5))
    ax1 = perhour.sum(axis=0).plot.line(lw=3,c='white')
    plt.ylim([0,1.1*perhour.sum(axis=0).max()])
    plt.xlabel('uur')
    plt.title('alle posts per tijdstip')
    recolorlineplot(ax1,color='white')
    plt.savefig('perhour.svg', dpi=150, transparent=True, bbox_inches='tight')
    plt.close()

    for year in perhour.index:
        perhour.loc[year,:] = perhour.loc[year,:]/perhour.loc[year,:].max()

    fig2 = plt.figure(figsize=(10,7.5))
    plt.imshow(perhour.transpose(), interpolation='spline16', aspect='auto', cmap='Wistia', origin='lower')
    plt.xticks(np.arange(0,len(perhour.index),1),perhour.index)
    plt.yticks(np.arange(-0.5,24,1),range(25))
    ax2 = plt.gca()
    recolormap(ax2,'white')
    plt.title('heatmap van posts door de dag over de jaren')
    plt.savefig('perhourmap.png', dpi=150, transparent=True, bbox_inches='tight')
    plt.close()

def forumhistogram():
    ppa = loadpickle('postsperauthor')
    df = pd.DataFrame.from_dict(ppa).set_index('author')

    plt.figure(figsize=(10,7.5))
    ax = df.iloc[:20,0].sort_values(ascending=True).plot.barh(color='white')
    recolorhist(ax, color='white')
    plt.xlim([0,8000])
    plt.xlabel('aantal posts voor de top 20 posters')
    plt.ylabel('')
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    plt.savefig('posthisttop20.svg', dpi=150, transparent=True, bbox_inches='tight')
    plt.close()

    ppp = loadpickle('postsperprins')
    df = pd.DataFrame.from_dict(ppp).set_index('naam').sort_values(by='posts', ascending=True)

    plt.figure(figsize=(10,7.5))
    ax = df.loc[:,'posts'].plot.barh(color='white')
    total = float(loadpickle('totals')['posts'])
    for p in ax.patches:
        ax.annotate('%.0f%%' % (p.get_width()/total*100), (50, p.get_y() + .18), color='#FF9900')
    recolorhist(ax, color='white')
    plt.xlim([0,8000])
    plt.xlabel('Totaal aantal posts per prins')
    plt.ylabel('')
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    plt.savefig('posthistogram.svg', dpi=150, transparent=True, bbox_inches='tight')
    plt.close()

    plt.figure(figsize=(10,7.5))
    ax = df.loc[:,'averagepostlength'].plot.barh(color='white')
    recolorhist(ax, color='white')
    plt.xlim([0,450])
    plt.xlabel('Gemiddelde lengte van alle posts')
    plt.ylabel('')
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    plt.savefig('postlenhistogram.svg', dpi=150, transparent=True, bbox_inches='tight')
    plt.close()

