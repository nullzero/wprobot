# -*- coding: utf-8  -*-
"""
Library to extract information from a service. Also clear the page
of service so that it is ready for next customer.
"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import pywikibot
import wp
from wp import lwikitable, linfo, lre

def glob():
    global patclear
    patclear = lre.lre(ur"(?ms)^(\!.*?$\n).*?(^\|\})")

def service(page, confpage, operation, verify, summary, debug=False):
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
    lastrev = int(linfo.getdat(confpage, operation))
    oldcontent = page.get()
    header, table = lwikitable.wiki2table(oldcontent)
    disable = [False] * len(table)
    hist = page.fullVersionHistory(total=100)
    # There is no need to get all revisions, just 100 is fine.

    for i, version in enumerate(hist):
        if version[0] == lastrev:
            hist = hist[:i+1]
            break

    hist.reverse()
    pywikibot.output("Processing %d revision(s)" % len(hist))
    for i in xrange(len(hist) - 1):
        oldv = hist[i][3]
        newv = hist[i + 1][3]
        usernew = hist[i + 1][2]
        try:
            dummy, cold = lwikitable.wiki2table(oldv)
            dummy, cnew = lwikitable.wiki2table(newv)
        except:
            wp.error()
            continue
        oldvc = set([wp.toutf(x) for x in cold])
        newvc = set([wp.toutf(x) for x in cnew])
        difference = [eval(x) for x in (newvc - oldvc)]
        if not verify(usernew):
            for entry in difference:
                for cnt, fentry in enumerate(table):
                    if entry == fentry:
                        disable[cnt] = True
                        break

    newcontent = patclear.sub(r"\1\2", oldcontent)

    if oldcontent != newcontent:
        if not debug:
            page = wp.Page(page.title())
            page.put(newcontent, summary())
            pywikibot.output(page.getVersionHistory(total=1)[0][0])
            linfo.putdat(confpage, operation, page.getVersionHistory()[0][0])

    return header, table, disable

glob()
