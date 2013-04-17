# -*- coding: utf-8  -*-
"""
Connect to API
"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import pywikibot
import wp
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

def append(page, text, comment=u'', minorEdit=True, botflag=True,
           async=False):
    # TODO: async support
    token = page.site.getToken("edit")
    r = api.Request(site=page.site,
                    action="edit",
                    title=page.title(),
                    appendtext=text,
                    summary=comment,
                    token=token)
                    
    if minorEdit:
        r["minor"] = ""
    if botflag:
        r["bot"] = ""
    
    try:
        r.submit()
    except:
        wp.error()

def parse(site, text):
    r = api.Request(site=site,
                    action="parse",
                    text=text)
    try:
        result = r.submit()
    except:
        wp.error()
    else:
        return result['parse']['text']['*']
