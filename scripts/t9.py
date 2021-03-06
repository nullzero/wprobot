#!/usr/bin/python
# -*- coding: utf-8  -*-
"""T9 Deleter"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import difflib
import init
import wp
import pywikibot
from wp import lnotify, lre, lrepeat

def glob():
    lre.pats["stripcomment"] = lre.lre(u"(?s):?\s*เนื้อหาเดิม.*")
    lre.pats["ref"] = lre.lre(u"(?ms)^== *อ้างอิง *==.*")

def cntref(text):
    return (text.count("<ref") + # inline citation
           (lre.pats["ref"].find(text) or "").count("http://") + # references in references section
           (lre.pats["ref"].find(text) or "").count("https://"))

def process(pagenow, page, user):
    if page is None:
        page = pagenow
    if (user.editCount() >= 5000 and "autoconfirmed" in user.groups()) or (
                                     "sysop" in user.groups()):
        return
    text = pagenow.get()
    nowrefs = cntref(text)
    pywikibot.output(">>> %s | %s with %d refs" %
                    (pagenow.title(), page.title(), nowrefs))
    ts = None
    for gen in site.deletedrevs(page, get_text=True, reverse=True):
        for rev in gen["revisions"]:
            ratio = difflib.SequenceMatcher(None, text, rev["*"]).ratio()
            oldrefs = cntref(rev["*"])
            pywikibot.output("processing %s; ratio %f; %d refs" %
                            (rev["revid"], ratio, oldrefs))
            if ratio >= 0.8:
                if nowrefs <= oldrefs:
                    ts = pywikibot.Timestamp.fromISOformat(rev["timestamp"])
                    break
                else:
                    pywikibot.output("refs has been improved")
        break

    if ts is None:
        return

    cntdel = 0
    first = True
    deletion = None
    for dl in site.logevents("delete", page=pagenow, reverse=True):
        cntdel += 1
        if dl.timestamp() > ts:
            if first:
                deletion = dl
                first = False

    if deletion is None:
        pywikibot.output("Weird")
        return

    reason = lre.pats["stripcomment"].sub("", deletion.comment()).strip()

    associatedPage = pagenow.toggleTalkPage()
    if associatedPage.exists():
        associatedPage.delete(reason=u"โรบอต: ลบหน้าพูดคุยของหน้าที่ถูกลบอัตโนมัติ", prompt=False)

    pagenow.delete(reason=u"โรบอต: %s" %
                  (reason or u"[[WP:CSD#ท9|ท9]]: สร้างหน้าที่เคยถูกลบใหม่"),
                  prompt=False)

    pywikibot.output("deleted")
    site.login()

    lnotify.notify("t9", user.getUserTalkPage(), {
                        "page": pagenow.title(),
                        "date": ts.strftime("%d/%m/%y %H:%M (UTC)"),
                        "pagefrom": "" if page == pagenow
                                       else u"ของหน้า " + page.title(),
                        "admin": deletion.user(),
                        "reason": (u' "{}"'.format(reason) if reason
                                                           else u"บางประการ"),
                    }, u"แจ้งเตือนการสร้างหน้าที่เคยถูกลบ", nocreate=False,
                    botflag=False)

    pywikibot.output(u"had deleted for {} times".format(cntdel))
    if cntdel >= 3:
        page.protect(edit=None, move=None, create="sysop", 
                     reason=u"โรบอต: หน้าไม่ผ่านเกณฑ์ - ถูกลบหลายครั้งติดต่อกัน", expiry="14 days", prompt=False)
        pywikibot.output("protected")

def main():
    page = wp.handlearg("page", args)
    if page:
        page = wp.Page(page)
        dic = page.getVersionHistory(reverseOrder=True, total=1)
        gen = [{"user": dic[0][2], "title": page.title()}]
        check = wp.handlearg("check", args)
        if check:
            check = wp.Page(check)
    else:
        gen = lrepeat.repeat(site, site.recentchanges, lambda x: x["revid"],
                             60, showRedirects=False, changetype=["new"],
                             showBot=False, namespaces=[0])
    for rev in gen:
        try:
            process(wp.Page(rev["title"]), check, wp.User(rev["user"]))
        except:
            wp.error()

args, site, conf = wp.pre(1, lock=False, continuous=True, main=__name__)
try:
    glob()
    wp.run(main)
except:
    wp.posterror()
else:
    wp.post()
