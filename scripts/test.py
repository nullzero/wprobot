# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from pywikibot import pagegenerators
from wp import lapi, lre

def glob():
    pass

def main():
    pass
    
if __name__ == "__main__":
    sites = [pywikibot.getSite("i18n", "i18n"), 
             pywikibot.getSite("wikidata", "wikidata"),
             pywikibot.getSite("th", "wikibooks"),
             pywikibot.getSite("th", "wikipedia"),]
    args, site, conf = wp.pre("test", sites=sites)
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        pass
        wp.post()
