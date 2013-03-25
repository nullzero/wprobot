# -*- coding: utf-8  -*-
"""Clear sandbox! Nothing more than this."""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot

def glob():
    pass

def main():
    if conf.modeClear == "only":
        pagelist = [wp.conf.sandboxPages[0]]
    else:
        pagelist = wp.conf.sandboxPages
    for title in pagelist:
        page = pywikibot.Page(site, title)
        page.put(conf.text, conf.summary)    
        
if __name__ == "__main__":
    args, site, conf = wp.pre("clearSandbox", lock=True)
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
