#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot

def main():
    for i in site.broken_redirects():
        print i

if __name__ == "__main__":
    args, site, conf = wp.pre(0)
    try:
        main()
    except:
        wp.posterror()
    else:
        wp.post()
