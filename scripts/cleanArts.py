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
    for arg in args:
        page = wp.handlearg("page", arg)
        if page:
            page = pywikibot.Page(site, page)
            page.put(lcleaner.clean(page.get()), conf.summary)
        else:
            print lcleaner.clean(arg)

if __name__ == "__main__":
    args, site, conf = wp.pre(u"clean articles")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
