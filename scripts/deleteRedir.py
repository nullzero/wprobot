# -*- coding: utf-8 -*-
"""Delete unnecessary redirect."""

__version__ = "1.0.0"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot

def glob():
    pass

def main():
    for ns in [x for x in range(1, 17, 2) if x not in [3, 5]]:
        gen = site.allpages(namespace=ns, filterredir=True)
        for i in gen:
            print i.title()
            i.delete(reason=u"โรบอต: หน้าเปลี่ยนทางไม่จำเป็น", prompt=False)

if __name__ == "__main__":
    args, site, conf = wp.pre("deleteRedir")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
