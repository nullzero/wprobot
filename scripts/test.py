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
    page = wp.Page(u'ไฟล์:Dekisugi.jpg')
    print list(page.backlinks())
    """
    for page in site.allpages(namespace=828):
        print page.title()
        if raw_input('protect [Y/n]: ') != 'n':
            page.protect(prompt=False, reason='โรบอต: แม่แบบ/มอดูลสำคัญ')
    """

args, site, conf = wp.pre(12, main=__name__)
try:
    wp.run(main)
except:
    wp.posterror()
else:
    wp.post()
