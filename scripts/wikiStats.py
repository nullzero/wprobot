#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import init
import wp
from wp import ldata, lre, lthread
import pywikibot

"""
Begin helper function
"""

def glob():
    global pageMain, contentMain
    pageMain = None
    contentMain = None
    lre.pats["tspan"] = lre.lre("<.*?>")

def firstContributor(page):
    name = page.getVersionHistory(reverseOrder=True, total=1)[0][2]
    if wp.User(name).isAnonymous():
        return "-"
    else:
        return u"[[User:%s|%s]]" % (name, name)

def getdat(regex):
    s = regex.find(contentMain)
    s = [x.strip() for x in s.split("|-")]
    table = []
    for line in s:
        line = line.strip()
        if line.startswith("|}"):
            break
        if not line.startswith("|"):
            continue
        table.append([x.strip() for x in line.split("||")])
    
    for i in xrange(len(table)):
        table[i][0] = lre.pats["link"].find(table[i][0])[2:-2]
    return table

def tag(x):
    if x == 0:
        return conf.same
    elif x < 0:
        return conf.inc
    else:
        return conf.dec

def writetable(table, regex):
    global contentMain
    for i in xrange(len(table)):
        table[i][0] = u"%s %d. [[%s]]" % (tag(i + 1 - table[i][1]), 
                                            i + 1, table[i][0])
        if table[i][1] == sys.maxint:
            table[i][1] = conf.newcomer
        table[i] = u" || ".join([unicode(x) for x in table[i]])
    contentMain = regex.sub(u"".join(map(lambda x: u"\n|-\n| " + x, table)) +
                        "\n|}\n{{hatnote|" + conf.summary + u" %s}}\n" % 
                        wp.getTime(), contentMain)

def flush():
    pywikibot.showDiff(pageMain.get(), contentMain)
    if raw_input("prompted: ") == "y":
        pageMain.put(contentMain, conf.summary)

def getrankold(title, table):
    for i, val in enumerate(table):
        if val[0] == title:
            return i + 1
    return sys.maxint

"""
End helper function
"""

def mosteditsArt():
    """
    most edits
    """
    regexArt = lre.genData(conf.tagind, u"บทความแก้ไขมากสุด")
    regexArtlist = lre.genData(conf.tagind, u"บทความรายชื่อแก้ไขมากสุด")
    oldtable = getdat(regexArt)
    oldtablelist = getdat(regexArtlist)
    table = []
    tablelist = []
    ptr = 0
    patListName = lre.lre(lre.sep(conf.listname))
    for page, revisions in site.mostrevisionspages():
        if len(tablelist) < 5 and patListName.search(page.title()):
            tablelist.append([page.title(),
                              getrankold(page.title(), oldtablelist),
                              revisions, 
                              firstContributor(page)])
        elif len(table) < 10 and not patListName.search(page.title()):
            table.append([page.title(),
                          getrankold(page.title(), oldtable),
                          revisions,
                          firstContributor(page)])
        elif (len(tablelist) >= 5) and (len(table) >= 10):
            break
            
    writetable(table, regexArt)
    writetable(tablelist, regexArtlist)
    
def longpages():
    """
    long pages
    """
    table = []
    regexLong = lre.genData(conf.tagind, u"บทความยาวสุด")
    oldlongpages = getdat(regexLong)
    for page, length in site.longpages(total=5):
        table.append([page.title(), getrankold(page.title(), oldlongpages),
                    length])
    writetable(table, regexLong)
    
def mosteditsUser():
    """
    most edits (user)
    """
    limit = lre.getconf(u"ตารางชาววิกิพีเดียที่เขียนมากที่สุด", contentMain)
    regexUser = lre.genData(conf.tagind, u"ชาววิกิพีเดียที่เขียนมากที่สุด")
    oldusers = getdat(regexUser)
    table = []
    for line in pywikibot.Page(site, conf.page500).get().split("\n"):
        libe = line.strip()
        if line == u"|-":
            continue
        if line.startswith(u"|"):
            line = [x.strip() for x in line[1:].split(u"||")]
            name = lre.pats["tspan"].sub("", 
                   lre.pats["link"].find(line[1])[2:-2])
            cnt = lre.pats["link"].find(line[2], "name")[1:]
            if int(cnt) < int(limit):
                break
            table.append([name, getrankold(name, oldusers), cnt])
    writetable(table, regexUser)
    
def main():
    global pageMain, contentMain
    pageMain = wp.Page(u"วิกิพีเดีย:ที่สุดในวิกิพีเดียภาษาไทย")
    contentMain = pageMain.get()
    mosteditsArt()
    longpages()
    mosteditsUser()
    flush()
    
args, site, conf = wp.pre(13, main=__name__)
try:
    glob()
    main()
except:
    wp.posterror()
else:
    wp.post()
