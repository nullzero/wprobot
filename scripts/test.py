# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from pywikibot import pagegenerators

def glob():
    pass

def main():
    pywikibot.output("abcdef")
        
if __name__ == "__main__":
    #sites = [("wikidata", "repo")]
    sites = []
    args, site, conf = wp.pre("test", sites=sites)
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        pass
        wp.post()
