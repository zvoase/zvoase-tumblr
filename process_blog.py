#! /usr/bin/env python
# -*- coding: utf-8 -*-

from xml.etree import ElementTree as element_tree
import re
import subprocess
import sys

import pygments
import pygments.formatters
import pygments.lexers


HIGHLIGHT_RE = re.compile(r'^highlight (?P<name>[^\s]+)$')


def get_lexer(name='text'):
    try:
        return pygments.lexers.get_lexer_by_name(name)
    except pygments.util.ClassNotFound:
        return pygments.lexers.get_lexer_by_name('text')

def highlight_html(data):
    data = u'<div class="post">\n' + data.decode('utf-8') + u'\n</div>'
    tree = element_tree.fromstring(stupefy(data))
    process_tree(tree)
    result = element_tree.tostring(tree, encoding='utf-8')
    return ''.join(result.splitlines(True)[1:-1]).strip()

def stupefy(string):
    mapping = {
        8211: '-',
        8212: '--',
        8216: "'",
        8217: "'",
        8220: '"',
        8221: '"',
        8230: '...',
    }
    for num, stupefied in mapping.items():
        string = string.replace('&#%d;' % (num,), stupefied)
        string = string.replace(unichr(num), stupefied)
    return string

def process_tree(tree):
    if (tree.tag != 'pre' or
        not HIGHLIGHT_RE.match(tree.attrib.get('class', ''))):
        for child in tree.getchildren():
            process_tree(child)
        return
    
    lexer = get_lexer(**HIGHLIGHT_RE.match(tree.attrib['class']).groupdict())
    formatter = pygments.formatters.get_formatter_by_name('html')
    code = tree.text.strip()
    highlighted = pygments.highlight(code, lexer, formatter)
    htree = element_tree.fromstring(highlighted)
    
    tree.clear()
    
    tree.tag = 'div'
    tree.attrib['class'] = 'highlight'
    tree.append(htree.find('pre'))

def smartypants(data, mode='1'):
    proc = subprocess.Popen('smartypants', stdin=subprocess.PIPE, 
                                           stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate(data)
    return stdout

def textile(data):
    proc = subprocess.Popen('textile.rb', stdin=subprocess.PIPE, 
                                          stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate(data)
    return stdout

def main():
    data = sys.stdin.read()
    sys.stdout.write(smartypants(highlight_html(textile(data))))

if __name__ == '__main__':
    main()
