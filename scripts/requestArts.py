# -*- coding: utf-8 -*-
"""
Update reqired articles at RECENTCHANGES page. The articles are obtained
from both WP:VITAL and WP:REQUEST.
"""

import init
import wp
import pywikibot
from random import shuffle
from wp import lre, lapi

def glob():
    global paten, patWOen, patlink, patoldlink, dummytext, patLI
    prepat = r"(?m)^[\*\#]+\s*\[\[(?!:en:)(.*?)(?:\|.*?)?\]\]"
    sufpat = r".*?\[\[(:en:.*?)\]\]"
    patoldlink = lre.lre(r"(?m)(^--> \[\[.*?\]\] <!--\n)+")
    patlink = lre.lre(r"(?m)(?<=^--> )\[\[.*\]\](?= <!--$)")
    patWOen = lre.lre(prepat)
    paten = lre.lre(prepat + sufpat)
    dummytext = "<!-- dummy for putting -->"
    patLI = lre.lre("(?<=<li>).*?(?=</li>)")

def getlink(page, lim, reqen=False):
    """Extract article's title from link in given page."""
    page = pywikibot.Page(site, page)
    content = page.get()
    content = content.replace(u"'''", u"")
    candidates = []
    regex = paten if reqen else patWOen
    for link in regex.finditer(content):
        if reqen:
            candidates.append((link.group(1), link.group(2)))
        else:
            candidates.append((link.group(1), None))
    shuffle(candidates)
    text = lapi.parse(site, "\n".join(
                      ["* {{PAGESIZE:%s|R}}" % page[0] for page in candidates]))
    count = 0
    out = []
    pagesize = patLI.findall(text)
    for i, link in enumerate(candidates):
        link, enlink = link
        if int(pagesize[i]) == 0:
            if enlink:
                out.append(u"[[%s]][[%s|^]]" % (link, enlink))
            else:
                out.append(u"[[%s]]" % link)
            count += 1
        if count == lim:
            break
    return out

def main():
    pagewrite = pywikibot.Page(site, conf.pagewrite)
    content = pagewrite.get()
    numlinks = len(patlink.findall(content))
    s = []
    s += getlink(conf.wpreq, numlinks // 2, reqen=True)
    s += getlink(conf.wpvital, numlinks - (numlinks // 2), reqen=True)
    content = patoldlink.sub(dummytext + u"\n", content)
    content = content.replace(dummytext, u"\n".join(
                              map(lambda x: u"--> " + x + u" <!--", s)))
    pagewrite.put(content, conf.summary)

if __name__ == "__main__":
    args, site, conf = wp.pre(u"update request articles", lock=True)
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
