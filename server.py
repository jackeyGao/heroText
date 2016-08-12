# -*- coding: utf-8 -*-
'''
File Name: server.py
Author: JackeyGao
mail: gaojunqi@outlook.com
Created Time: 四  8/11 11:38:45 2016
'''
import json
import arrow
from itertools import chain
from collections import defaultdict
from collections import Counter
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from pagination import Pagination
from db import Post

app = Flask(__name__)
PER_PAGE = 15
TIMEZONE = "UTC"

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)


def humanize(time):
    if time is None:
        return None
    return arrow.get(time, TIMEZONE).humanize()


def get_instances_for_page(page, per_page, posts):
    pages = [ 
        posts[i:i+per_page] \
        for i in xrange(0, len(posts), per_page)
    ]
    return pages[page - 1]


@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def index(page):
    tag = request.args.get('tag', '')
    query = Post.select().where(
            Post.tags.contains(tag)
            ).order_by(Post.time.desc())
    count = len(query)
    posts = get_instances_for_page(page, PER_PAGE, query)
    pagination = Pagination(page, PER_PAGE, count) 
    return render_template('posts.html', **locals())


@app.route('/tags/')
def tags():
    tags = [ post.get_tags() for post in Post.select() ]
    tags = json.dumps(dict(Counter(list(chain(*tags)))))
    return render_template('tags.html', **locals())


@app.route('/archives/')
def archives():
    data = defaultdict(list)
    posts = Post.select().order_by(Post.time.desc())

    for post in posts:
        data[post.time.year].append(post)

    return render_template('archives.html', **locals())


app.jinja_env.globals['to_page'] = url_for_other_page
app.jinja_env.globals['humanize'] = humanize

if __name__ == "__main__":
    app.run()
