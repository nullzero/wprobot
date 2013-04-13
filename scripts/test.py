# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from wp import lnotify

def glob():
    pass

def main():
    lnotify.notify("dpl", u"วิกิพีเดีย:ทดลองเขียน", {
                                  "links": """; abc
* asd
* dsa
; qwe
* 123
* 312"""
                                }, u"ทดสอบการแจ้งเตือนผู้ใช้")

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
