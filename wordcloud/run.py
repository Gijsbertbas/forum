import re
from wordcloud import WordCloud
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import random

# FOR WORDCLOUD
def postswordcloud(reload=False):

    def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

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
                    max_words=5000, 
                    mask=mask, 
                    stopwords=stops,
                    max_font_size=40,
                    scale=5
                    )
    wc.generate(text)
    wc.to_file('forumwordcloud.png')
    
    plt.figure(figsize=(10,10))
    plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3), cmap='gray', interpolation='bilinear')
    plt.axis('off')
    plt.savefig('forumwordcloud_r.png', dpi=300)
    plt.close()
    
'''
for prins in prinsennamen:
    for ps in prins['pseudoniemen']:
        try:
            posterslist.remove(ps)
        except:
            print('not in')

'''
