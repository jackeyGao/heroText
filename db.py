# -*- coding: utf-8 -*-
'''
File Name: db.py
Author: JackeyGao
mail: gaojunqi@outlook.com
Created Time: 四  8/11 14:33:38 2016
'''
from peewee import *

db = SqliteDatabase('post.db')
db.connect()

class Post(Model):
    filename = CharField()
    time = DateTimeField()
    title = CharField()
    tags = CharField()
    content = TextField()

    class Meta:
        primary_key = CompositeKey('title')
        database = db

    def get_tags(self):
        return self.tags.split(',')

if __name__ == '__main__':
    db.create_tables([Post,])
