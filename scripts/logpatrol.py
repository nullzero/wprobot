# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from wp import ltime, lre
from collections import deque

def glob():
    lre.pats["trim"] = r"\{\{test\d?\}\}\s*"

def getconfig():
    exec("\n".join(wp.Page(u"ผู้ใช้:Nullzerobot/ปูมการละเมิด").get()
                                                         .splitlines()[1:-1]))
    return config

def main():
    user = {}
    config = getconfig()
    pywikibot.output(config)
    site.login(sysop=True)
    seen = set()
    start = site.getcurrenttime()
    while True:
        for i in config:
            for ab in site.abuselog(reverse=True, abuseid=i, start=start):
                if (ab["user"], ab["timestamp"]) in seen:
                    continue
                seen.add((ab["user"], ab["timestamp"]))
                pywikibot.output("filter: %s\t\tuser: %s\t\ttime: %s" %
                            (i, ab["user"].ljust(16), ab["timestamp"]))
                if ab["user"] not in user:
                    user[ab["user"]] = {}
                if i not in user[ab["user"]]:
                    user[ab["user"]][i] = deque()
                deq = user[ab["user"]][i]
                deq.append(pywikibot.Timestamp.fromISOformat(ab["timestamp"]))
                now = site.getcurrenttime()
                while deq and ((now - deq[0]).seconds >= config[i][0]):
                    deq.popleft()
                pywikibot.output(list(deq))
                if len(deq) >= config[i][1]:
                    pywikibot.output("Block!")

                    userobj = wp.User(ab["user"])
                    if userobj.isRegistered():
                        userobj.block(u"โรบอต: ก่อกวน ดูปูมการละเมิด",
                                        expiry=config[i][2])
                    else:
                        userobj.block(u"โรบอต: ก่อกวน ดูปูมการละเมิด",
                                        expiry="1 day")
                    deq.clear()
                    pagetalk = userobj.getUserTalkPage()
                    pagetalk.put("{{test5}} --~~~~\n" +
                                 lre.pats["trim"].sub("", pagetalk.get()),
                                 u"โรบอต: แจ้งการถูกบล็อก")

        ltime.sleep(60)
        start = max(start, site.getcurrenttime() - ltime.td(seconds=120))

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
