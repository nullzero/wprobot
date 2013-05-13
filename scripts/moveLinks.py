# -*- coding: utf-8  -*-
"""Move links!"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from wp import lre

def glob():
    pass

def main():
    if len(args) != 2:
        return
    pagemain = wp.Page(wp.toutf(args[0]))
    newlink = wp.toutf(args[1])
    pywikibot.output("old: " + pagemain.title())
    pywikibot.output("new: " + newlink)
    for page in pagemain.backlinks(content=True):
        pywikibot.output("processing " + page.title())
        txt = page.get()
        page.put(lre.sub(r"\[\[" + lre.escape(pagemain.title()),
                         "[[" + newlink.replace("_", " "), txt), u"ย้ายลิงก์ไปหน้าใหม่")

if __name__ == "__main__":
    args, site, conf = wp.pre("move links")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        pass
        wp.post()
