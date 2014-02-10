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
    site.login(False)
    print site.user()
    print api.Request(site=pywikibot.getSite("th"), action='query', meta='allmessages|siteinfo', 
                      ammessages="abusefilter-accountreserved|january").submit()
    
if __name__ == "__main__":
    args, site, conf = wp.pre(12)
    try:
        main()
    except:
        wp.posterror()
    else:
        wp.post()
