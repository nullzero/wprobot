# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot

def glob():
    pass

def main():
    now = site.getcurrenttime()
    for user in site.allusers():
        if user["registration"]:
            now = min(now, pywikibot.Timestamp.fromISOformat(user["registration"]))
        print user["name"], user["registration"]
        print now

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
