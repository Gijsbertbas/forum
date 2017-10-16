# Forum #
This is a little **private** hobby project using Scrapy and Django to rebuild the message board of 'de Prinsen'. 

*the original*
![Screenshot of the original](forumillustrations/forumoriginal.jpg)

### Objective ###
The objectives were:
* Learn how to use Scrapy and practice my Django skills
* Document this piece of 'nostalgia' in case the original host dies
* NOT to re-build full functionality (e.g. re-enable posting new messages)

## Forumscrape ##
This is the scrapy project to download and store all posts in a database. I had to extract the tree structure of the forum and save it using django-items.

## Forumreborn ##
This is the Django project which rebuilds the site. I implemented an MP-tree from django treebeard project. In here you also find extractfacts.py which saves some summarizing data into a pickle file.

*the rebuild*
![Screenshot of the rebuild](forumillustrations/forumreborn.jpg)

## Forumillustrations ##
This folder contains some code to make figures for the 'facts 'n figures' page. Figures are created using pandas/matplotlib and the excellent [wordcloud package by amueller](https://github.com/amueller/word_cloud).

I have forked the original to add the option of transparency. Install the forked version with:

    pip install git+git://github.com/Gijsbertbas/word_cloud_transparent.git@master

### Requirements ###
I installed the following packages in my conda environment
* django==1.11.3
* django-treebeard==4.1.2
* matplotlib==2.0.2
* numpy==1.13.1
* pandas==0.20.3
* pillow==4.2.1
* python==3.5.4
* scrapy==1.3.3
* wordcloud==1.3.1 *(as described above)*
