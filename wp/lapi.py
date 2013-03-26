# -*- coding: utf-8  -*-
"""
Connect to API
"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import pywikibot
from pywikibot.data import api
from wp import lre

def extractLinkedPages(site, text, title=None, expand=False):
    """
    This function extract linked pages.
    """
    if not expand:
        links = []
        for link in lre.pats["link"].finditer(text):
            links.append(u"[[" + link.group("title") + u"]]")
        text = "".join(links)
    
    r = api.Request(site=site,
                    action="parse",
                    text=text,
                    prop="links")
                    
    if title:
        r["title"] = title
    
    return [pywikibot.Page(site, item['*'])
            for item in r.submit()['parse']['links']]
