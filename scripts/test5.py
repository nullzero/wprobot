#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from pywikibot.data import api
import re
#from pywikibot.pagegenerators import RepeatingGenerator

def escape(s):
    return s.replace('\n', '\\n').replace('\t', '\\t')

def main():
    site = pywikibot.Site('commons', 'commons')
    cat = pywikibot.Category(site, "Images from Wiki Loves Monuments 2014 in Thailand")
    cnt = 0
    group = 0
    for file in cat.articles(namespaces=[6], content=True):
        nt = re.sub(r'(?s)(.*?)\s*$',
                    r'\1\n' + '[[Category:Images from Wiki Loves Monuments 2014 in Thailand/Group {}]]'.format(
                        chr(ord('A') + group)
                    ), file.text)
        if nt != file.text:
            file.text = nt
            file.save('Bot: categorize images from WLM2014 Thailand')
            
        cnt += 1
        if cnt == 858:
            group += 1
            cnt = 0
    
args, site, conf = wp.pre(12, main=__name__)
try:
    wp.run(main)
except:
    wp.posterror()
else:
    wp.post()
