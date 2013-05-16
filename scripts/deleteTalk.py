# -*- coding: utf-8 -*-
"""Delete unnecessary redirect."""

__version__ = "1.0.0"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from pywikibot.tools import itergroup

def glob():
    pass

def process(lst):
    exist = site.pagesexist([x.toggleTalkPage().title() for x in lst])
    for i, page in enumerate(lst):
        if "/" in page.title():
            pywikibot.output("subpage " + page.title())
        if not exist[i][0]:
            if (page.botMayEdit() and
                    (site.getcurrenttime() - page.editTime()).days >= 30):
                pywikibot.output("deleting " + page.title())
                if raw_input("... ") == "y":
                    page.delete(reason=u"โรบอต: หน้าขึ้นกับหน้าว่าง", prompt=False)
            else:
                pywikibot.output("can't delete " + page.title())

def main():
    namespaces = [x for x in range(1, 16, 2) if x not in [3, 5]]
    for ns in namespaces:
        gen = site.allpages(namespace=ns, filterredir=True)
        for i in gen:
            pywikibot.output("deleting " + i.title())
            i.delete(reason=u"โรบอต: หน้าเปลี่ยนทางไม่จำเป็น", prompt=False)

    for ns in namespaces:
        pywikibot.output("ns " + str(ns))
        gen = site.allpages(namespace=ns, content=True)
        for i, pages in enumerate(itergroup(gen, 5000)):
            pywikibot.output("processing bunch %d" % i)
            process(pages)

if __name__ == "__main__":
    args, site, conf = wp.pre("deleteRedir")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
