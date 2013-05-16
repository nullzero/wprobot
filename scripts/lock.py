#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Lock page when edits war occured"""

__version__ = "1.0.0"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from collections import deque
from wp import ltime, lrepeat

def glob():
    global storage
    storage = {}

def normalizeText(s):
    return s

def check(revision):
    title = revision["title"]
    pywikibot.output(u"check page %s @ %s | %s" % (title, revision["timestamp"], revision["user"]))
    revid = revision["revid"]
    ts = pywikibot.Timestamp.fromISOformat(revision["timestamp"])
    page = wp.Page(title)
    text = page.getOldVersion(revid)
    if title not in storage:
        storage[title] = deque()
    stitle = storage[title]
    stitle.append((normalizeText(text), ts, revision["user"]))
    #while((ts - stitle[0][1]).seconds >= 60 * 60 * 6):
    while ((ts - stitle[0][1]).seconds >= 60 * 60 * 12) and (len(stitle) > 10):
        stitle.popleft()
    checkr = set()
    userr = set()
    for i in stitle:
        checkr.add(i[0])
        userr.add(i[2])
    print len(stitle), len(checkr), len(userr)
    if (len(stitle) >= 8) and (len(stitle) - len(checkr) >= 5) and (len(userr) > 1):
        print "lock!"
        """
        page.protect(u"โรบอต: ย้อนเนื้อหาไปมาจำนวนมาก", locktype="edit",
                                              duration={"hours": 5},
                                              level="autoconfirmed")
        """
        stitle.clear()

def main():
    gen = lrepeat.repeat(site, site.recentchanges, lambda x: x["revid"], 60,
                         showRedirects=False, changetype=["edit", "new"],
                         showBot=False, namespaces=[0],
                         start=site.getcurrenttime() - ltime.td(hours=1))
    for rev in gen:
        try:
            check(rev)
        except:
            wp.error()
            pass

if __name__ == "__main__":
    args, site, conf = wp.pre("lock page")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()

a/b < c
