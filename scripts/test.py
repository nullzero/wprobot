#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot

def main():
    #wp.Page(u"User talk:Nullzero/กระบะทราย").delete(reason="asd", prompt=False)
    wp.Page(u"User talk:Nullzero/กระบะทราย").move(u"User talk:Nullzero/กระบะทราย3", "test")
    
if __name__ == "__main__":
    args, site, conf = wp.pre(0)
    try:
        main()
    except:
        wp.posterror()
    else:
        wp.post()
