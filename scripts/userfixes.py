# -*- coding: utf-8 -*-
"""
Fix misspelled words
"""

import init
import wp
import pywikibot
from wp import lre

def glob():
    global subst
    subst = lre.subst()
    #subst.append((u"(?<!วัด)ทรง(เสวย|ประชวร|มีพระ|เป็นพระ|เสด็จ|บรรทม|ผนวช|ทอดพระเนตร|สวรรคต)", r"\1"))
    #subst.append((u"== *แหล่งอื่น *==", u"== แหล่งข้อมูลอื่น =="))
    subst.append((ur"\{\{\s*([Bb]abel|บาเบล)\s*\|", "{{#babel:"))

def fix(s):
    return subst.process(s)

def main():
    tl = [wp.Page(u"ผู้ใช้:Girmitya"), wp.Page(u"ผู้ใช้:Thakurji")]
    #tl = wp.Page(u"Template:บาเบล")
    #for page in site.allpages(filterredir=False, content=True):
    #for page in tl.embeddedin(content=True):
    for page in tl:
        #page = wp.Page(u"รายชื่อวัดในจังหวัดชัยนาท")
        pywikibot.output(">>>" + page.title())
        text = fix(page.get())
        if page.get() != text:
            pywikibot.showDiff(page.get(), text)
            try:
                page.put(text, u"โรบอต: ปรับปรุงแม่แบบ", async=True)
            except:
                wp.error()
                pass

if __name__ == "__main__":
    args, site, conf = wp.pre(u"user-fixes")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
