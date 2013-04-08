# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from wp import lapi

def glob():
    pass

def main():
    page = wp.Page(u'วิกิพีเดีย:ทดลองเขียน')
    page.put(u"asd" * 20, "asd")
    
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
