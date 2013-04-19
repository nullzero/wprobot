# -*- coding: utf-8  -*-
"""T9 Deleter"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import difflib
import init
import wp
import pywikibot
from wp import lgenerator, lnotify, lprotect

def glob():
    pass

def process(rev):
    user = wp.User(rev["user"])
    if (user.editCount() >= 5000 and "autoconfirmed" in user.groups()) or (
                                     "sysop" in user.groups()):
        return
    page = wp.Page(rev["title"])
    pywikibot.output(">>> " + page.title())
    text = page.get()
    tstext = None
    for gen in site.deletedrevs(page, get_text=True, reverse=True):
        for rev in gen["revisions"]:
            ratio = difflib.SequenceMatcher(None, text, rev["*"]).ratio()
            pywikibot.output("processing %s; ratio %f" % (rev["revid"], ratio))
            if ratio >= 0.9:
                page.delete(reason=u"[[WP:CSD#ท9|ท9]]: สร้างหน้าที่เคยถูกลบใหม่",
                            prompt=False)
                pywikibot.output("deleted")
                site.login()
                tstext = pywikibot.Timestamp.fromISOformat(rev["timestamp"])
                break
        break

    if tstext is None:
        return

    cntdel = 0
    first = True
    deletion = None
    for dl in site.logevents("delete", page=page, reverse=True):
        cntdel += 1
        if dl.timestamp() > tstext:
            if first:
                deletion = dl
                first = False

    if deletion is None:
        pywikibot.output("Weird")
        return

    lnotify.notify("t9", user.getUserTalkPage(), {
                        "page": page.title(),
                        "date": rev["timestamp"],
                        "admin": deletion.user(),
                        "reason": deletion.comment(),
                    }, u"แจ้งเตือนการสร้างหน้าที่เคยถูกลบ", nocreate=False,
                    botflag=False, async=True)

    pywikibot.output(u"had deleted for %d times" % cntdel)
    if cntdel >= 5:
        lprotect.protect(site, page, u"หน้าไม่ผ่านเกณฑ์ - ถูกลบหลายครั้งติดต่อกัน",
                         locktype="create", period={"days": 14},
                         level="sysop")
        pywikibot.output("protected")
        site.login()

def main():
    for rev in lgenerator.recentchanges(site,
                                        showRedirects=False,
                                        changetype=["new"],
                                        showBot=False,
                                        namespaces=[0],
                                        repeat=True):
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
