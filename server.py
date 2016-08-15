# -*- coding: utf-8 -*-
'''
File Name: server.py
Author: JackeyGao
mail: gaojunqi@outlook.com
Created Time: 四  8/11 11:38:45 2016
'''
import json
import arrow
from dateutil import tz
from commands import getstatusoutput
from itertools import chain
from collections import defaultdict
from collections import Counter
from flask import Flask
from flask import send_from_directory
from flask import abort
from flask import render_template
from flask import request
from flask import url_for
from peewee import DoesNotExist
from pagination import Pagination
from db import Post
from markdown import markrender
from parse import parse_all, save

app = Flask(__name__)
PER_PAGE = 15
TIMEZONE = "Asia/Shanghai"

def url_for_other_page(page):
    params = dict(request.args.copy())
    args = request.view_args.copy()
    params.update(args)
    params['page'] = page
    return url_for(request.endpoint, **params)


def humanize(time):
    if arrow.get(time, TIMEZONE) > arrow.now(TIMEZONE):
        return "Sticky Post"

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


@app.route('/post/<string:title>')
def post(title):
    try:
        post = Post.select().where(Post.title==title).get()
    except DoesNotExist:
        abort(404)
    return render_template('post.html', **locals())


@app.route('/uploads/<path:path>')
@app.route('/down/<path:path>')
def uploads(path):
    return send_from_directory('uploads', path)

@app.route('/update', methods=['POST', 'GET'])
def update():
    getstatusoutput('git pull origin master')
    parse_all('./uploads/_posts/', save)
    return "OK"

app.jinja_env.globals['to_page'] = url_for_other_page
app.jinja_env.globals['humanize'] = humanize
app.jinja_env.globals['markrender'] = markrender

if __name__ == "__main__":
    app.run()
