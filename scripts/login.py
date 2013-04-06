# -*- coding: utf-8  -*-
"""Login"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from pywikibot import config

def glob():
    pass

def main():
    pass
        
if __name__ == "__main__":
    args, site, conf = wp.pre("login")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        pass
        wp.post()
