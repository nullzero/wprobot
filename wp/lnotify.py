# -*- coding: utf-8  -*-
"""
Data structure library.
"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import random
import init
import wp
from wp import lre, lapi

def glob():
    lre.pats["subtl"] = lre.lre("\{\{\{(.*?)\}\}\}")

def notify(template, page, dic, summary, nocreate=True, botflag=True):
    text = None
    force = random.randint(0, 64) == 0
    if force or hasattr(notify, "_template"):
        if force or template in notify._template:
            text = notify._template[template]
    else:
        notify._template = {}

    if text is None:
        text = wp.Page(wp.conf.notifyMessage + "/" + template).get()
        notify._template[template] = text

    process = lambda x: lre.pats["subtl"].sub(r"%(\1)s",
                        x.replace("<!---->", ""))

    lapi.append(page, "\n\n" + (process(text) % dic) + "--~~~~", summary,
                minorEdit=False, botflag=botflag, nocreate=nocreate)

glob()
