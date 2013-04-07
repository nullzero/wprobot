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

def firstContributor(title):
    name = pywikibot.Page(site, title).getCreator()[0]
    if wp.User(name).isAnonymous():
        return "-"
    else:
        return u"[[User:%s|%s]]" % (name, name)

def pagestat(): 
    allpages = ldata.LimitedSortedList(lambda a, b: b[0] - a[0])
    pool = lthread.ThreadPool(10)
    
    def localAdd(_allpages, _page):
        _allpages.append((len(_page.getVersionHistory()), _page.title()))
        
    for page in site.allpages(filterredir=False):
        pywikibot.output(u">>> %s" % page.title())
        pool.add_task(localAdd, allpages, page)
    pool.wait_completion()
    
    return allpages.get()

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
        print table[i][0]
        table[i][0] = (lre.pats["link"].find(table[i][0], "title") + 
                       lre.pats["link"].find(table[i][0], "name"))
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
    allpages = pagestat()
    while True:
        if (len(tablelist) < 5) and patListName.search(allpages[ptr][1]):
            tablelist.append([allpages[ptr][1], getrankold(allpages[ptr][1],
                                                            oldtablelist), 
                        allpages[ptr][0], firstContributor(allpages[ptr][1])])
        elif len(table) < 10 and (not patListName.search(allpages[ptr][1])):
            table.append([allpages[ptr][1], getrankold(allpages[ptr][1], 
                                                        oldtable), 
                        allpages[ptr][0], firstContributor(allpages[ptr][1])])
        elif (len(tablelist) >= 5) and (len(table) >= 10):
            break
        ptr += 1
            
    writetable(table, regexArt)
    writetable(tablelist, regexArtlist)
    
def longpages():
    """
    long pages
    """
    table = []
    regexLong = lre.genData(conf.tagind, u"บทความยาวสุด")
    oldlongpages = getdat(regexLong)
    print oldlongpages
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
            name = (lre.pats["link"].find(line[1], "title") +
                    lre.pats["link"].find(line[1], "name"))
            cnt = lre.pats["link"].find(line[2], "name")
            if int(cnt[1:]) < int(limit):
                break
            table.append([name, getrankold(name, oldusers), cnt])
    writetable(table, regexUser)
    
def main():
    global pageMain, contentMain
    pageMain = pywikibot.Page(site, u"วิกิพีเดีย:ที่สุดในวิกิพีเดียภาษาไทย")
    contentMain = pageMain.get()
    #mosteditsArt()
    longpages()
    mosteditsUser()
    flush()
    
if __name__ == "__main__":
    args, site, conf = wp.pre(u"update top things in Wikipedia")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
