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
    pages = ["A", "adsads", "B", "dsadsa"]
    text = lapi.parse(site, "\n".join(
                      ['* ("%(page)s", {{PAGESIZE:%(page)s|R}}, %(en)s)' % 
                      {"page": page[0], } for page in pages]))
    for line in lre.findall("(?<=<li>).*?(?=</li>)", text):
        dat = eval(line)
        if dat[1] > 0:
            
    
if __name__ == "__main__":
    args, site, conf = wp.pre("test")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        pass
        wp.post()
