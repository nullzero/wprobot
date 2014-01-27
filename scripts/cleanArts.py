#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
Clean pages which are given in argument list. If there is no argument,
it will clean sample text instead. To configure the cleaning, pleas look
at wp.lcleaner
"""

__version__ = "2.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from wp import lcleaner

def glob():
    pass

def main():
    page = wp.handlearg("page", args)
    if page:
        page = wp.Page(page)
        page.put(lcleaner.clean(page.get()), conf.summary)
    txt = wp.handlearg("txt", args)
    if txt:
        pywikibot.output(lcleaner.clean(txt))

if __name__ == "__main__":
    args, site, conf = wp.pre(u"clean articles")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
