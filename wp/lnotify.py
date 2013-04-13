# -*- coding: utf-8  -*-
"""
Data structure library.
"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import random
import init
import wp
from wp import lre

def glob():
    lre.pats["subtl"] = lre.lre("\{\{\{(.*?)\}\}\}")

def notify(template, page, dic, summary, nocreate=True):
    text = None
    force = random.randint(0, 27) == 0
    if hasattr(notify, "_template") or force:
        if template in notify._template or force:
            text = notify._template[template]
    else:
        notify._template = {}

    if text is None:
        text = wp.Page(wp.conf.notifyMessage + "/" + template).get()
        notify._template[template] = text

    process = lambda x: lre.pats["subtl"].sub(r"%(\1)s",
                        x.replace("<!---->", ""))

    page.put(page.get() + "\n\n" + (process(text) % dic) + "--~~~~",
             summary, minorEdit=False, async=True)

glob()
