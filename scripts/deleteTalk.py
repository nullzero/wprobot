# -*- coding: utf-8 -*-
"""Delete unnecessary redirect."""

__version__ = "1.0.0"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot

def glob():
    pass

def process(lst):
    exist = site.pagesexist([x.toggleTalkPage().title() for x in lst])
    for i, page in enumerate(lst):
        pywikibot.output("checking " + page.title())
        if "/" in page.title():
            continue
        if not exist[i][0]:
            page.delete(reason=u"โรบอต: หน้าขึ้นกับหน้าว่าง", prompt=False)

def main():
    namespaces = [x for x in range(1, 16, 2) if x not in [3, 5]]
    for ns in namespaces:
        gen = site.allpages(namespace=ns, filterredir=True)
        for i in gen:
            pywikibot.output("deleting " + i.title())
            i.delete(reason=u"โรบอต: หน้าเปลี่ยนทางไม่จำเป็น", prompt=False)

    for ns in namespaces:
        lst = []
        for page in site.allpages(namespace=ns):
            lst.append(page)
            if len(lst) >= conf.step:
                process(lst[:conf.step])
                del lst[:conf.step]
    process(lst)

if __name__ == "__main__":
    args, site, conf = wp.pre("deleteRedir")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
