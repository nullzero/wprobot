#!/usr/bin/python
# -*- coding: utf-8 -*-
"""To update 500 top users who edit Wikipedia most."""

import init
import wp
import pywikibot
from wp import lre, ldata

def glob():
    pass

def isbot(data):
    return (("bot" in data["groups"]) or
            any([pati.search(data["name"]) for pati in conf.patbot]))

def dowrite(path, data, activedata):
    pretext = u"ปรับปรุงล่าสุด %s\n\n{{/begin|500}}\n" % wp.getTime()
    entry = []
    cnt = 1

    for i in data:
        entry.append(u"|-\n| %(cnt)d || [[User:%(name)s|%(op)s%(name)s%(ed)s]]"
                     u" %(sys)s %(bot)s || [[Special:Contributions/%(name)s"
                     u"|%(edit)s]]\n" % {
                        "cnt":  cnt,
                        "name": i["name"],
                        "sys":  "(Admin)" if ("sysop" in i["groups"]) else "",
                        "bot":  "(Bot)" if isbot(i) else "",
                        "edit": i["editcount"],
                        "op": '<span style="color:grey">' if
                              (i["name"] not in activedata) else '',
                        "ed": '</span>' if
                              (i["name"] not in activedata) else '',
                    })
        cnt += 1

    page = pywikibot.Page(site, path)
    gettext = page.get()

    dummy, posttext = gettext.split(u"{{/end}}")

    page.put(pretext + "".join(entry) + "{{/end}}" + posttext, conf.summary)
    pywikibot.output("done!")

def main():
    funcSortedList = lambda a, b: b["editcount"] - a["editcount"]
    includelist = ldata.LimitedSortedList(funcSortedList)
    excludelist = ldata.LimitedSortedList(funcSortedList)
    cntuser = 0
    for user in site.allusers():
        if cntuser % conf.maxnum == 0:
            pywikibot.output(u"processing (%d): %s" % (cntuser // conf.maxnum,
                                                       user["name"]))
        includelist.append(user)
        if not isbot(user):
            excludelist.append(user)
        cntuser += 1

    activedata = set()

    for user in site.allusers(onlyActive=True):
        activedata.add(user["name"])

    dowrite(conf.path + conf.botsuffix,
            includelist.get()[:conf.allentries],
            activedata)
    dowrite(conf.path,
            excludelist.get()[:conf.allentries],
            activedata)

args, site, conf = wp.pre(8, lock=True, main=__name__)
try:
    glob()
    wp.run(main)
except:
    wp.posterror()
else:
    wp.post()
