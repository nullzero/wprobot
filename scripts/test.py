#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from wp import ltime

def glob():
    pass

def main():
    while True:
        print "a"
        ltime.sleep(1)
        raise NotImplementedError

if __name__ == "__main__":
    args, site, conf = wp.pre(1, lock=True)
    try:
        glob()
        wp.run(main)
    except:
        wp.posterror()
    else:
        wp.post()
