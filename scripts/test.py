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
    wp.Page(u'คุยกับผู้ใช้:Nullzero/กระบะทราย').protect(u'ทดสอบ API', locktype='edit', expiry='1 day', level='sysop')
    
if __name__ == "__main__":
    args, site, conf = wp.pre(12)
    try:
        main()
    except:
        wp.posterror()
    else:
        wp.post()
