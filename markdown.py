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
        if ctext.startswith('center\n') and ctext.endswith('\ncenter'):
            text = ""
            for t in ctext.splitlines():
                if t.strip() == 'center':
                    continue

                text += '<p>%s</p>\n' % t.strip()

            return '<blockquote class="blockquote-center">%s</blockquote>' % text
        return '<blockquote class="blockquote-normal">%s</blockquote>' % text

    def image(self, link, title="", alt=''):
        if title:
            return '<p><img src="%s" alt="%s"></p>\n<p class="img-title">"%s"</p>' % (link, alt, title)
        else:
            return '<p><img src="%s" alt="%s"></p>\n' % (link, alt)



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

