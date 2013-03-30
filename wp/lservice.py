# -*- coding: utf-8  -*-
"""
Library to extract information from a service. Also clear the page
of service so that it is ready for next customer.
"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import pywikibot
from wp import lwikitable, linfo, lre

def glob():
    patclear = lre.lre(ur"(?ms)^(\!.*?$\n).*?(^\|\})")

def service(page, confpage, operation, verifyFunc, summary, 
            debug=False):
    """
    Get:
        Service page
        Key to read from config page,
        Function to verify user
        Config page
        Site
        Summary function.

    Function:
        Clear service's page

    Return:
        Header of table
        List of rows
        Suspicious entry(/row)
    """
    lastrev = int(linfo.getdat(key=operation, wikipage=confpage))
    oldcontent = page.get()
    header, table = lwikitable.wiki2table(oldcontent)
    disable = [False] * len(table)
    hist = page.getVersionHistory()
    # There is no need to get all revisions, just 500 is fine (by default).
    histlist = []

    for version in hist:
        histlist.append((version, page.getOldVersion(version[0])))
        if hist:
            break
        if version[0] == lastrev:
            break
    hist = histlist
    hist.reverse()
    pywikibot.output(u"Processing %d revision(s)" % len(hist))
    for i in xrange(len(hist) - 1):
        oldv = hist[i][1]
        newv = hist[i + 1][1]
        usernew = hist[i + 1][0][2]
        dummy, cold = lwikitable.wiki2table(oldv)
        dummy, cnew = lwikitable.wiki2table(newv)
        oldvc = set([wp.toutf(x) for x in cold])
        newvc = set([wp.toutf(x) for x in cnew])
        difference = [eval(x) for x in (newvc - oldvc)]
        if not verifyFunc(usernew):
            for entry in difference:
                for cnt, fentry in enumerate(table):
                    if entry == fentry:
                        disable[cnt] = True
                        break

    newcontent = patclear.sub(ur"\1\2", oldcontent)

    if oldcontent != newcontent:
        if not debug:
            page = pywikibot.Page(page)
            page.put(newcontent, summary())
        
        pywikibot.output(page.getVersionHistory()[0][0])
        linfo.putdat(key=operation, 
                       value=page.getVersionHistory()[0][0], 
                       wikipage=confpage)
                        
    return header, table, disable

glob()
