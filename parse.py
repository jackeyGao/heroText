# -*- coding: utf-8 -*-
'''
File Name: parse.py
Author: JackeyGao
mail: gaojunqi@outlook.com
Created Time: 四  8/11 10:15:14 2016
'''
import os
import yaml
from peewee import *
from db import Post
from db import db

@db.atomic()
def save(headers, content, post):
    headers["time"] = headers["date"]
    headers.pop("date")
    if isinstance(headers["tags"], list):
        tags = [ t for t in headers['tags'] ]
        headers["tags"] = ','.join(tags)
    else:
        headers["tags"] = headers["tags"]

    headers["content"] = content
    headers["filename"] = post

    allow_keys = ('time', 'title', 'tags', 'content', 'filename')
    for key in headers.keys():
        if key not in allow_keys:
            headers.pop(key)

    try:
        post = Post.create(**headers)
        print("The post (%s) was created!" % post.title)
    except IntegrityError as e:
        q = Post.update(**headers).where(Post.title==headers["title"])
        q.execute()
        print("The post (%s) was updated!" % headers["title"])


def parse_all(posts_dir, save_callback):
    for post in os.listdir(posts_dir):
        path = os.path.join(posts_dir, post)

        if not path.endswith('.md'):
            continue

        with open(path, 'r') as md:
            header, content = md.read().split('\n---\n')

        save(yaml.load(header), content, post)


if __name__ == '__main__':
    parse_all('./uploads/_posts/', save)
