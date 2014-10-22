#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from pywikibot.data import api

def main():
    '''
    # content / transclusion / withSortKey, withSortHidden
    list(wp.Page(u'กระจุกดาวเปิด').categories(content=False, withSortKey=False, withHidden=False, transclusion=False))
    print 'EXPECT: NONE\n'
    
    list(wp.Page(u'กระจุกดาวเปิด').categories(content=True, withSortKey=False, withHidden=False, transclusion=False))
    print 'EXPECT: PAGE\n'
    
    list(wp.Page(u'กระจุกดาวเปิด').categories(content=False, withSortKey=True, withHidden=False, transclusion=False))
    print 'EXPECT: NONE\n'
    
    list(wp.Page(u'กระจุกดาวเปิด').categories(content=False, withSortKey=False, withHidden=True, transclusion=False))
    print 'EXPECT: PROPERTY\n'
    
    list(wp.Page(u'กระจุกดาวเปิด').categories(content=False, withSortKey=True, withHidden=True, transclusion=False))
    print 'EXPECT: PROPERTY\n'
    
    list(wp.Page(u'กระจุกดาวเปิด').categories(content=True, withSortKey=False, withHidden=True, transclusion=False))
    print 'EXPECT: BOTH\n'
    
    list(wp.Page(u'กระจุกดาวเปิด').categories(content=True, withSortKey=True, withHidden=False, transclusion=False))
    print 'EXPECT: PAGE\n'
    
    list(wp.Page(u'กระจุกดาวเปิด').categories(content=True, withSortKey=True, withHidden=True, transclusion=False))
    print 'EXPECT: BOTH\n'
    '''
    '''
    list(wp.Page(u'กระจุกดาวเปิด').categories(content=False, withSortKey=True, withHidden=True, transclusion=True))
    print 'EXPECT: PROPERTY\n'
    '''
    '''
    out = []
    for i in range(0, 3000, 10):
        out.append(u'[[หมวดหมู่:พุทธทศวรรษ {}]]'.format(i))
    
    page = wp.Page(u'User:Nullzero/กระบะทราย')
    page.text = '\n'.join(out)
    page.save(as_group='sysop')
    '''
    
    with open('/Users/nullzero/Desktop/UQ.txt', 'r') as f:
        content = f.read()
    
    l = []
    
    for line in content.split('\n'):
        l.append(line.split('\t'))
        
    site = pywikibot.Site('commons', 'commons')
    
    cat = pywikibot.Category(site, 'Cultural_heritage_monuments_in_Thailand_with_known_IDs')
    
    import re
    
    for page in cat.articles(content=True):
        print page
        text = page.text
        for replace, search in l:
            text = text.replace(search, replace)
        
        text = re.sub("\|\s*-00-0001\s*\}", "|5675}", text)
        text = re.sub("\|\s*-01-0001\s*\}", "|5660}", text)
        
        if text != page.text:
            page.text = text
            page.save(u'Bot: correct monument ID (WLM Thailand)', async=True)
        
    

args, site, conf = wp.pre(12, main=__name__)
try:
    wp.run(main)
except:
    wp.posterror()
else:
    wp.post()
