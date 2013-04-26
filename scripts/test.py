# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from wp import lre

def glob():
    pass

def main():
    page = wp.Page(wp.conf.sandboxPages[0])
    page.change_category(wp.Category("abcdef"), wp.Category("qwerty"), inPlace=True)

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
