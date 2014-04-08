#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
import os
import urllib

def main():
    aliases = [u"กล่องข้อมูล ภาพชอบธรรม",
               "nonfreeimage",
               "Nonfreeimage",
               "Non-free use rationale",
               "non-free use rationale",
               u"กล่องข้อมูล ไฟล์ชอบธรรม"]
    for page in site.unusedfiles():
        if not page.exists(): continue
        text = page.get()
        for name in aliases:
            if name in text:
                os.system(("open /Applications/Google\ Chrome.app/"
                            " http://th.wikipedia.org/wiki/{}").format(
                            urllib.quote(page.title().encode('utf-8'))))
                if raw_input() != 'n':
                    page.delete(reason=u"โรบอต: ไฟล์ชอบธรรมไม่มีการใช้งาน", prompt=False)
                    break

if __name__ == "__main__":
    args, site, conf = wp.pre(12)
    try:
        main()
    except:
        wp.posterror()
    else:
        wp.post()
