# -*- coding: utf-8  -*-
"""
Repeat fetching info!
"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
from wp import ltime

def repeat(site, func, keyfunc, wait, **kwargs):
    start = None
    if "start" in kwargs:
        start = kwargs["start"]
        del kwargs["start"]
    start = start or site.getcurrenttime()
    seen = set()
    while True:
        gen = func(start=start, reverse=True, **kwargs)
        for item in gen:
            key = keyfunc(item)
            if key not in seen:
                seen.add(key)
                yield item

        ltime.sleep(wait)
        start = max(start, site.getcurrenttime() - ltime.td(seconds=2*wait))
