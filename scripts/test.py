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
    i = 0
    while True:
        pywikibot.output(i)
        i += 1
        if i == 3:
            raise NotImplementedError
        ltime.sleep(10)

if __name__ == "__main__":
    args, site, conf = wp.pre(1)
    try:
        glob()
        wp.run(main)
    except:
        wp.posterror()
    else:
        pass
        wp.post()
