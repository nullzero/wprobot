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
    """
    for page in site.allpages(namespace=828):
        print page.title()
        if raw_input('protect [Y/n]: ') != 'n':
            page.protect(prompt=False, reason='โรบอต: แม่แบบ/มอดูลสำคัญ')
    """

    """
    page = wp.Page(u'ผู้ใช้:Nullzero/กระบะทราย3')
    page.protect(edit=None, move=None, create='sysop', reason='test', prompt=False)
    """
    """
    for page in site.getAll([wp.Page('Template:!'), wp.Page('Template:((')]):
        print page.text
    """
    
    s = """
Babel 	
Category handler/blacklist 	
Category handler/config 	
Category handler/data 	
Category handler/shared 	
Check for unkwn parameters 	
Episode list 	
Gaps 	
Location map/data/Afghanistan 	
Location map/data/Alaska 	
Location map/data/Albania 	
Location map/data/Algeria 	
Location map/data/Belgium 	
Location map/data/Croatia 	
Location map/data/France 	
Location map/data/Germany 	
Location map/data/Iran 	
Location map/data/Iraq 	
Location map/data/Italy 	
Location map/data/Nepal 	
Location map/data/New York 	
Location map/data/Pennsylvania 	
Location map/data/Poland 	
Location map/data/Slovenia 	
Location map/data/Syria 	
Location map/data/USA 	
Location map/data/USA Alaska 	
Location map/data/USA New York 	
Location map/data/USA Oregon 	
Location map/data/USA Pennsylvania 	
Middleclass 	
Module overview 	
Plotter/DefaultColors 	
Portal 	
Su 	
Subject bar
"""
    for page in s.split('\n'):
        page = page.strip()
        if not page: continue
        print u"""###############################

page = u'Module:{page}'

config[page] = {{
    'source': u'en:Module:{page}',
    'users': ['Nullzero', 'Taweetham'],
    'findText': [],
    'addParam': [],
    'obsolete': [],
}}

###############################""".format(page=page)
    '''
    '''
    site.login(True)
    pageids = [516429, 516430, 516433, 566073]
    for pageid in pageids:
        print pageid
        token = site.token(wp.Page('Main page'), "delete")
        req = api.Request(site=site, action="delete", token=token,
                          pageid=pageid,
                          reason=u'ลบหน้าที่ไม่สามารถเข้าถึงได้')
        try:
            result = req.submit()
        except api.APIError as err:
            raise
    '''
    for cat in wp.Page(u'กระจุกดาวเปิด').categories(transclusion=False, withSortKey=True):
        print 'cat', cat
        print 'sortkey', cat.sortKey
        print 'hidden', cat.hidden
        print 'timestamp', cat.timestamp
        print '-' * 10

args, site, conf = wp.pre(12, main=__name__)
try:
    wp.run(main)
except:
    wp.posterror()
else:
    wp.post()
