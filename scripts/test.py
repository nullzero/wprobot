# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from wp import lthread

def glob():
    pass

def main():
    l = wp.conf.sandboxPages
    pool = lthread.ThreadPool(10)
    for i in xrange(20):
        page = wp.Page(l[i % len(l)])
        page.text = "abcdef " * (10 + i)
        pool.add_task(site.editpage, page, "test")
        print "put " + page.title()
    pool.wait_completion()

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
