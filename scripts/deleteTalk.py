#!/usr/bin/python
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
        if not exist[i][0]:
            if "/" in page.title():
                if page.parentPage().toogleTalkPage().exists():
                    continue
                elif wp.handlearg("manual", args):
                    continue

            if (page.botMayEdit() and
                    (site.getcurrenttime() - page.editTime()).days >= 30):
                pywikibot.output("deleting " + page.title())
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

args, site, conf = wp.pre(3, lock=True, main=__name__)
try:
    glob()
    wp.run(main)
except:
    wp.posterror()
else:
    wp.post()
