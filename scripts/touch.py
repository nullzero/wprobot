# -*- coding: utf-8 -*-
"""example"""

__version__ = "1.0.0"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from wp import lthread

def glob():
    pass

def main():
    if args:
        for page in wp.Category(wp.toutf(args[0])).articles(content=True):
            page.save("null edit", async=True)

if __name__ == "__main__":
    args, site, conf = wp.pre("null edit")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
