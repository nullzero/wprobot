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
    ref = wp.Page("cat year nav")
    for page in ref.embeddedin(content=True):
        text = page.get()
        if u"ก่อตั้งในปี" in text:
            page.put(text.replace(u"องค์กร", u"องค์การ"), "เปลี่ยนหมวดหมู่")

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
