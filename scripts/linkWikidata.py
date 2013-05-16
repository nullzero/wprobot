#!/usr/bin/python
# -*- coding: utf-8 -*-
"""example"""

__version__ = "1.0.0"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from wp import lthread

def glob():
    global ensite
    ensite = pywikibot.getSite(code="en")

def main():
    def local(page):
        pywikibot.output(">>> " + page.title())
        enpage = pywikibot.Page(ensite, page.title(withNamespace=False),
                                ns=page.namespace())
        item = pywikibot.ItemPage.fromPage(enpage)
        testitem = pywikibot.ItemPage.fromPage(page)
        if (item.exists() and not testitem.exists() and
                              site.dbName() not in item.get()["sitelinks"]):
            item.editEntity({'sitelinks': {site.dbName(): {'site': site.dbName(),
                                                'title': page.title()}},
                         'labels': {site.code: {'language': site.code,
                                                'value': page.title()}}})

    pool = lthread.ThreadPool(10)
    for page in site.allpages(namespace=10):
        pool.add_task(local, page)
    pool.wait_completion()

if __name__ == "__main__":
    args, site, conf = wp.pre("null edit")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
