# -*- coding: utf-8 -*-
'''
File Name: markdown.py
Author: JackeyGao
mail: gaojunqi@outlook.com
Created Time: 五  8/12 09:59:17 2016
'''
import sys, re
import misaka as m
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

reload(sys)
sys.setdefaultencoding('utf-8')

cleanr =re.compile('<.*?>')

class HighlighterRenderer(m.HtmlRenderer):
    def blockcode(self, text, lang):
        if not lang:
            return '''\n<div class="highlight"><pre>{}</pre></div>\n'''.format(
                text.strip())

        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()

        return highlight(text, lexer, formatter)


    def blockquote(self, text):
        ctext = re.sub(cleanr,'', text).strip()
        if ctext.startswith('%center\n'):
            ctext = ctext.replace('%center', '')
            className = "blockquote-center"
        elif ctext.startswith('%warning'):
            ctext = ctext.replace('%warning', '')
            className = "blockquote-warning"
        elif ctext.startswith('%error'):
            ctext = ctext.replace('%error', '')
            className = "blockquote-error"
        else:
            className = "blockquote-normal"
        
        text = ""
        for t in ctext.splitlines():
            text += '<p>%s</p>\n' % t.strip()

        return '<blockquote class="%s">%s</blockquote>' % (className, text)

    def image(self, link, title="", alt=''):
        if title:
            return '<p><img src="%s" alt="%s"></p>\n<div class="img-title"><span>%s</span></div>' % (link, alt, title)
        else:
            return '<p><img src="%s" alt="%s"></p>\n' % (link, alt)

    def table(self, content):
        print content
        return '<table class="ui selectable celled table">' + content + '</table>'



markdown = m.Markdown(
    HighlighterRenderer(),
    extensions=\
    m.EXT_FENCED_CODE |\
    m.EXT_TABLES |\
    m.EXT_QUOTE
)

#toc = m.Markdown(m.HtmlTocRenderer())

def markrender(content):
    return markdown(content)

if __name__ == '__main__':
    print markrender('你好, 我是**JackeyGao**')

