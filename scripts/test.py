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
    print wp.User("Nullzero").name()

if __name__ == "__main__":
    args, site, conf = wp.pre(1)
    try:
        glob()
        wp.run(main)
    except:
        wp.posterror()
    else:
        wp.post()
