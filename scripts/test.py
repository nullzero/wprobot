#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot

def glob():
    pass

def main():
    for page in site.allpages(prefix=u"พระจักรพรรดิ", filterredir=True):
        pageReal = page.getRedirectTarget()
        for bPage in page.backlinks(content=True):
            bPage.put(bPage.get().replace(page.title(), pageReal.title()),
                      u"โรบอต: แก้ไขคำผิด (แจ้งโดยคุณเอ็ดมัน)", async=True)
        if len(list(page.backlinks())) > 0: continue
        page.delete(reason=u"ชื่อผิด (แจ้งโดยคุณเอ็ดมัน)", prompt=False)

if __name__ == "__main__":
    args, site, conf = wp.pre(1)
    try:
        glob()
        wp.run(main)
    except:
        wp.posterror()
    else:
        wp.post()
