# -*- coding: utf-8  -*-
"""Clear sandbox! Nothing more than this."""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from pywikibot import pagegenerators
from wp import lre, ltime

def glob():
    pass

def main():
    print ltime.date.today().day
        
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
