#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Detect all unused template.
"""

__version__ = "1.0.0"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from wp import lthread
from pywikibot.data import api

def glob():
    pass

def main():
    r = api.Request(site=self.site, action="query", list="allfileusages", title=self.title(),
                    appendtext=text, summary=comment, token=token)
    '''
    for page in site.allpages(namespace=10):
        has = False
        for t in page.embeddedin():
            has = True
            break
        if not has:
            if "/" in page.title() and "/doc" not in page.title():
                print page.title()
            """
            if "/doc" in page.title():
                page.delete(reason=u"โรบอต: หน้าเปลี่ยนทางไม่จำเป็น", prompt=False)
            """
    '''
    

if __name__ == "__main__":
    args, site, conf = wp.pre("detect unused templates")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
