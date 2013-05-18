#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Block user by monitoring patrol log"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from wp import ltime, lre, lnotify
from collections import deque

def glob():
    pass

def process(user, data, ab):
    page = None
    summary = data["summary"]
    if data["action"] in ["block", "notifyUser"]:
        page = user.getUserTalkPage()
    elif data["action"] == "notify":
        page = wp.Page(data["pageReport"])

    if data["action"] == "block":
        expiry = "1 day"
        if user.isRegistered():
            if "blockDuration" in data:
                expiry = data["blockDuration"]
        else:
            if "anonBlockDuration" in data:
                expiry = data["anonBlockDuration"]
        try:
            user.block(u"โรบอต: " + data["summary"], expiry=expiry)
        except NotImplementedError:
            return
        summary = u"แจ้งการถูกบล็อก: " + summary

    if page is not None:
        lnotify.notify(data["template"], page, {
                            "user": user.name(),
                            "title": ab["title"],
                       }, u"โรบอต: " + summary, nocreate=False)

def main():
    user = {}
    seen = set()
    start = site.getcurrenttime()
    config = wp.ReadCode(wp.Page(u"ผู้ใช้:Nullzerobot/ปูมการละเมิด"), "config")
    while True:
        config.load()
        for i in config.data:
            data = config.data[i]
            for ab in site.abuselog(reverse=True, abuseid=i, start=start):
                if (ab["user"], ab["timestamp"]) in seen:
                    continue
                seen.add((ab["user"], ab["timestamp"]))
                pywikibot.output("filter: %s\t\tuser: %s\t\ttime: %s" %
                                (i, ab["user"].ljust(16), ab["timestamp"]))
                userobj = wp.User(ab["user"])
                if userobj.editCount() >= 5000:
                    continue
                if userobj.name() not in user:
                    user[userobj.name()] = {}
                if i not in user[userobj.name()]:
                    user[userobj.name()][i] = deque()
                deq = user[userobj.name()][i]
                deq.append(pywikibot.Timestamp.fromISOformat(ab["timestamp"]))
                now = site.getcurrenttime()
                while deq and ((now - deq[0]).seconds >= data["checkDuration"]):
                    deq.popleft()
                pywikibot.output(list(deq))
                if len(deq) >= data["threshold"]:
                    process(userobj, data, ab)
                    deq.clear()
                site.login(sysop=True)

        ltime.sleep(60)
        start = max(start, site.getcurrenttime() - ltime.td(seconds=120))

if __name__ == "__main__":
    args, site, conf = wp.pre(2, lock=False, continuous=True)
    try:
        glob()
        wp.run(main)
    except:
        wp.posterror()
    else:
        wp.post()
