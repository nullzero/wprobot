#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from pywikibot.data import api
#from pywikibot.pagegenerators import RepeatingGenerator

def escape(s):
    return s.replace('\n', '\\n').replace('\t', '\\t')

def main():
    """
    with open('file.txt', 'w') as f:
        lis = [u'ชื่อ', u'ภาพ', u'FADlink', u'ที่ตั้ง', u'ตำบล', u'อำเภอ', u'lat', u'lon',
               u'ประกาศ', u'ทะเบียน', u'หมายเหตุ', u'ลิงก์', u'GG', u'number', u'description']
        for i in lis:
            f.write(i.encode('utf-8') + '\t')
        f.write('อื่น ๆ\n')
        seen = {}
        for page in site.allpages(prefix=u'รายชื่อโบราณสถานใน', content=True):
            for (template, args) in page.templatesWithParams():
                if template.title(withNamespace=False) == u'แถวโบราณสถาน':
                    if page not in seen:
                        seen[page] = True
                        f.write('>>> ' + page.title().encode('utf-8') + '\n')
                    dic = {}
                    for arg in args:
                        a, b = arg.split('=')
                        a = escape(a.strip())
                        b = escape(b.strip())
                        dic[a] = b
                    for i in lis:
                        if i in dic:                    
                            f.write(dic.pop(i).encode('utf-8') + '\t')
                        else:
                            f.write('\t')
                    for i in dic:
                        f.write(i.encode('utf-8') + '=' + dic[i].encode('utf-8') + ' ')
                    f.write('\n')
    """
    for page in site.recentchanges(reverse=True):
        #print page
        print page
    """
    site = pywikibot.Site('en')
    page = pywikibot.Page(site, 'A')
    print api.Request(
        site=site,
        action="edit",
        token=site.token(page, "edit"),
        title=u"On2 gauge",
        appendtext=""
    ).submit()
    """
    
args, site, conf = wp.pre(12, main=__name__)
try:
    wp.run(main)
except:
    wp.posterror()
else:
    wp.post()
