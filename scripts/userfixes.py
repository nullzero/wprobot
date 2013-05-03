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
    subst.append((u"(?<!วัด)ทรง(เสวย|ประชวร|มีพระ|เป็นพระ|เสด็จ|บรรทม|ผนวช|ทอดพระเนตร|สวรรคต)", r"\1"))
    subst.append((u"== *แหล่งอื่น *==", u"== แหล่งข้อมูลอื่น =="))

def fix(s):
    return subst.process(s)

def main():
    for page in site.allpages(filterredir=False, content=True):
        #page = wp.Page(u"รายชื่อวัดในจังหวัดชัยนาท")
        text = fix(page.get())
        if page.get() != text:
            pywikibot.showDiff(page.get(), text)
            page.put(text, u"โรบอต: แก้ไขคำผิด", async=True)
        break

if __name__ == "__main__":
    args, site, conf = wp.pre(u"user-fixes")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
