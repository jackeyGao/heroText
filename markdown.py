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
            return '''
        \n<div class="highlight"><pre>{}</pre></div>\n'''.format(
                text.strip())

        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()

        return highlight(text, lexer, formatter)


    def blockquote(self, content):
        _real = re.sub(cleanr,'', content).strip()
        if _real.startswith('%center\n'):
            content = content.replace('%center', '')
            className = "blockquote-center"
        elif _real.startswith('%warning'):
            content = content.replace('%warning', '')
            className = "blockquote-warning"
        elif _real.startswith('%error'):
            content = content.replace('%error', '')
            className = "blockquote-error"
        else:
            content = content
            className = "blockquote-normal"
        
        content = content.replace('\n', '<br/>')
        content = content.replace('</p><br/>', '</p>')
        content = content.replace('<p><br/>', '<p>')

        return '''<blockquote class="%s">
                %s</blockquote>''' % (className, content)

    def image(self, link, title="", alt=''):
        if title:
            return  '''
                    <p><img src="%s" alt="%s"></p>
                    <div class="img-title">
                        <span>%s</span>
                    </div>''' % (link, alt, title)
        else:
            return '<p><img src="%s" alt="%s"></p>\n' % (link, alt)

    def table(self, content):
        return '<table class="ui selectable celled table">'\
                + content + '</table>'


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
    print markrender('''> %center''')
