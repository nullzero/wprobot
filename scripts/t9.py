# -*- coding: utf-8  -*-
"""T9 Deleter"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import difflib
import init
import wp
import pywikibot
from wp import lgenerator

def glob():
    pass

def process(rev):
    user = wp.User(rev["user"])
    if (user.editCount() >= 5000 and "autoconfirmed" in user.groups()) or (
                                     "sysop" in user.groups()):
        return
    page = wp.Page(rev["title"])
    print ">>>", page.title()
    text = page.get()
    for gen in site.deletedrevs(page, get_text=True):
        for rev in gen["revisions"]:
            ratio = difflib.SequenceMatcher(None, text, rev["*"]).ratio()
            print "processing", rev["revid"], "; ratio", ratio
            if ratio >= 0.9:
                page.delete(reason=u"ทดสอบ: [[WP:CSD#ท9|ท9]]: สร้างหน้าที่เคยถูกลบใหม่",
                            prompt=False)
                print "deleted"

                lnotify.notify("t9", user.getUserTalkPage(), {
                                }, u"สร้างหน้าที่เคยถูกลบ", nocreate=False,
                                botflag=False)
                    usertalk.put(u"%s\n\n%s --~~~~" % (usertalk.get(), message),
                                 , minorEdit=False, async=True)
                break
        break


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
