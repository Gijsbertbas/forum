# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-09 11:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ForumMessageModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('timestamp', models.DateTimeField()),
                ('network54ID', models.IntegerField()),
                ('network54URL', models.URLField()),
                ('hasparent', models.BooleanField(default=False)),
                ('parentID', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
