# -*- coding: utf-8 -*-
"""example"""

__version__ = "1.0.0"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot

def glob():
    pass

def main():
    NotImplemented

if __name__ == "__main__":
    args, site, conf = preload.pre("example", lock=True)
    try:
        glob()
        main()
    except:
        preload.posterror()
    else:
        preload.post()
