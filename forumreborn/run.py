from forum.models import ForumMessageModel
import re

# FOR WORDCLOUD
def postswordcloud(reload=False):

    if reload:
        output = open('posts.dat','a')
        for post in ForumMessageModel.objects.all():
            output.write(post.body[65:-36])
        output.close()

        text = open('posts.dat').read()
        text = re.sub('<([^<>]+)>','',text)
        text = re.sub('\n','',text)
        with open('posts.dat','w') as output:
            output.write(text)

'''
for prins in prinsennamen:
    for ps in prins['pseudoniemen']:
        try:
            posterslist.remove(ps)
        except:
            print('not in')

'''