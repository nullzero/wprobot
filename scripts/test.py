# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from wp import lre

def glob():
    pass

def main():
    for i in site.recentchanges(showRedirects=False, repeat=True,
                                start=site.getcurrenttime() - datetime.timedelta(seconds=600)):
        print i

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
