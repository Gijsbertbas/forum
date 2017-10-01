for prins in prinsennamen:
    for ps in prins['pseudoniemen']:
        try:
            posterslist.remove(ps)
        except:
            print('not in')

# FOR WORDCLOUD
output = open('posts.dat','a')
for post in ForumMessageModel.objects.all():
    output.write(post.body[65:-36])
output.close()

text = open('posts.dat').read()

words=['<br>','je','de','het','een','ik','je','naar','<a href=','</a>']

for word in words:
    text.replace(word,'')
    
with open('text.dat','w') as output:
    output.write(text)


