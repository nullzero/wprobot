# -*- coding: utf-8 -*-
"""To update 500 top users who edit Wikipedia most."""

import init
import wp
import pywikibot
from wp import lre, ldata, lapi

def glob():
    pbot = lre.lre(u"(?i)^(.*(บอต|bot)|(บอต|bot).*)$")

def isbot(data):
    if "bot" in data["groups"]: return True
    if data["name"] == u"New user message": return True
    return pbot.search(data["name"]) is not None

def dowrite(path, data):
    puttext = u"ปรับปรุงล่าสุด %s\n\n{{/begin|500}}\n" % wp.getTime()
    ptext = u""
    cnt = 1
    
    for i in data:
        ptext += (u"|-\n| %d || [[User:%s|%s]]" % (cnt, i["name"], i["name"]) +
            u" %s %s || " % ("(Admin)" if ("sysop" in i["groups"]) else "",
                            "(Bot)" if ("bot" in i["groups"]) else "") + 
            u"[[Special:Contributions/%s|%s]]\n" % (i["name"], i["editcount"]))
        cnt += 1
    
    page = pywikibot.Page(site, path)
    gettext = page.get()
    
    pre, post = gettext.split(u"{{/end}}")
    
    page.put(ptext + u"{{/end}}" + post, u"ปรับปรุงรายการ")
    pywikibot.output(u"done!")
    
def main():
    funcSortedList = lambda a, b: b["editcount"] - a["editcount"]
    includelist = ldata.LimitedSortedList(funcSortedList)
    excludelist = ldata.LimitedSortedList(funcSortedList)
    cntuser = 0
    for user in site.allusers():
        if cntuser % conf.maxnum == 0:
            pywikibot.output(u"processing (%d): %s" % (cntuser / conf.maxnum,
                                                       user["name"])
        includelist.append(user)
        if not isbot(user):
            excludelist.append(user)
            
    """
    dowrite(conf.path + conf.botsuffix, includelist.get()[:conf.allentries])
    dowrite(conf.path, excludelist.get()[:conf.allentries])
    """

if __name__ == "__main__":
    raise NotImplementedError
    args, site, conf = wp.pre("update top users who edit most",
                              lock=True)
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
