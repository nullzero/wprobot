#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from pywikibot.data import api

def inspect(page):
    print page
    print 'title', page.title()
    print 'namespace', page.namespace()
    print 'site', page.site

def main():
    inspect(wp.Page('th:abc'))
    inspect(wp.Page(':th:abc'))
    inspect(wp.Page('en:abc'))
    inspect(wp.Page(':en:abc'))
    inspect(wp.Page('s:abc'))
    inspect(wp.Page(':s:abc'))
    inspect(wp.Page('s:en:abc'))
    inspect(wp.Page(':s:en:abc'))
    inspect(wp.Page('s:th:abc'))
    inspect(wp.Page(':s:th:abc'))

args, site, conf = wp.pre(12, main=__name__)
try:
    wp.run(main)
except:
    wp.posterror()
else:
    wp.post()
