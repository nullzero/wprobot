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
    #print list(pywikibot.Page(pywikibot.getSite("af"), "Maan").iterlanglinks())
    for i in (site._generator(api.PageGenerator, type_arg="langbacklinks", lbllang="aa")):
        print i
    
if __name__ == "__main__":
    args, site, conf = wp.pre(12)
    try:
        main()
    except:
        wp.posterror()
    else:
        wp.post()
