# -*- coding: utf-8  -*-
"""Clear sandbox! Nothing more than this."""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import time
import init
import wp
import pywikibot
from pywikibot import pagegenerators
from wp import lthread

def glob():
    pass

cnt = 0

def fun(n, aaa):
    try:
        global cnt
        cnt += 1
        for i in xrange(n, -1, -1):
            print str(n) + " # " + str(i) + " " + str(n // i) + str(aaa)
            time.sleep(1)
    except:
        pass

def main():
    pool = lthread.ThreadPool(30)
    for i in xrange(4, -1, -1):
        pool.add_task(fun, i, 321123)
        print "abc"
    print ">>>", cnt
    pool.wait_completion()
    print ">>>", cnt
        
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
