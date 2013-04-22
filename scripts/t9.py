# -*- coding: utf-8  -*-
"""T9 Deleter"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import difflib
import init
import wp
import pywikibot
from wp import lnotify, lre

def glob():
    lre.pats["stripcomment"] = lre.lre(u"(?s):?\s*เนื้อหาเดิม.*")

def process(rev):
    user = wp.User(rev["user"])
    if (user.editCount() >= 5000 and "autoconfirmed" in user.groups()) or (
                                     "sysop" in user.groups()):
        return
    page = wp.Page(rev["title"])
    pywikibot.output(">>> " + page.title())
    text = page.get()
    ts = None
    for gen in site.deletedrevs(page, get_text=True, reverse=True):
        for rev in gen["revisions"]:
            ratio = difflib.SequenceMatcher(None, text, rev["*"]).ratio()
            pywikibot.output("processing %s; ratio %f" % (rev["revid"], ratio))
            if ratio >= 0.8:
                ts = pywikibot.Timestamp.fromISOformat(rev["timestamp"])
                break
        break

    if ts is None:
        return

    cntdel = 0
    first = True
    deletion = None
    for dl in site.logevents("delete", page=page, reverse=True):
        cntdel += 1
        if dl.timestamp() > ts:
            if first:
                deletion = dl
                first = False

    if deletion is None:
        pywikibot.output("Weird")
        return

    reason = lre.pats["stripcomment"].sub("", deletion.comment()).strip()

    page.delete(reason=u"โรบอต: %s" %
                (reason or u"[[WP:CSD#ท9|ท9]]: สร้างหน้าที่เคยถูกลบใหม่"),
                prompt=False)

    pywikibot.output("deleted")
    site.login()

    lnotify.notify("t9", user.getUserTalkPage(), {
                        "page": page.title(),
                        "date": ts.strftime("%d/%m/%y %H:%M (UTC)"),
                        "admin": deletion.user(),
                        "reason": (u' "%s"' % reason if reason
                                                     else u"บางประการ"),
                    }, u"แจ้งเตือนการสร้างหน้าที่เคยถูกลบ", nocreate=False,
                    botflag=False, async=True)

    pywikibot.output(u"had deleted for %d times" % cntdel)
    if cntdel >= 3:
        page.protect(u"หน้าไม่ผ่านเกณฑ์ - ถูกลบหลายครั้งติดต่อกัน",
                     locktype="create", duration={"days": 14},
                     level="sysop")
        pywikibot.output("protected")
        site.login()

def main():
    if args:
        page = wp.Page(wp.toutf(args[0]))
        dic = page.getVersionHistory(reverseOrder=True, total=1)
        gen = [{"user": dic[0][2], "title": page.title()}]
    else:
        gen = site.recentchanges(showRedirects=False, changetype=["new"],
                                 showBot=False, namespaces=[0], repeat=True)
    for rev in gen:
        try:
            process(rev)
        except:
            wp.error()

if __name__ == "__main__":
    args, site, conf = wp.pre("T9 Deleter", lock=True)
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
