#!/usr/bin/python
# -*- coding: utf-8  -*-
"""DYKChecker!"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import difflib
import json
import init
import wp
import pywikibot
import time
from wp import lre

def glob():
    global anchorBegin, anchorEnd, subst, anchor

    anchor = ur"[\uE000-\uF8FF]"
    anchorBegin = int("E000", 16)
    anchorEnd = int("F8FF", 16)

    subst = lre.subst()

    # delete inline ref
    subst.append((r"(?s)<ref[^>]*?/ *>", ""))
    subst.append((r"(?s)<ref.*?</ref>", ""))

    # delete external links
    subst.append((r"(?s)(?<!\[)\[(?!\[) *http://.*?\]", ""))
    subst.append((r"http://\S*", ""))

    # delete gallery
    subst.append((r"(?is)<gallery.*?>.*?</gallery>", ""))

    # delete non article links, must be called before deleting links
    subst.append((r"(?is)\[\[[^\]\|]*?\:.*?\]\]", ""))

    # delete links
    subst.append((r"\[\[[^\[\|]*?\|(.*?)\]\]", r"\1"))
    subst.append((r"[\[\]]", ""))

    # delete other markup
    subst.append(("\'{2,}", ""))

    # delete header
    subst.append((ur"(?m)^(%(s)s)\=+.*?\=+ *(%(s)s)$" % {"s": anchor}, r"\1\2"))

    # delete list
    subst.append((ur"(?m)^(%(s)s)[\:\*\#]*" % {"s": anchor}, r"\1"))

def showdiff(a, b):
    out = []
    match = False
    i, j = 0, 0

    while i < len(a) and j < len(b):
        if match != (a[i] == b[j]):
            match = not match
            out += list("~~~OPENSESAME~~~") if match else list("~~~CLOSESESAME~~~")
        out.append(a[i])
        i += 1
        j += int(match)

    return "".join(filter(lambda x: ord(x) < anchorBegin,
                   out + list("~~~CLOSESESAME~~~" if match else "") + list(a[i:])))

def rem(text):
    # delete table -- TODO: ^\{\{ or ^[\*\:\#]*\{\{
    text = lre.rmsym(r"\{\|", r"\|\}", text)
    # delete template
    text = lre.rmsym(r"\{\{", r"\}\}", text)

    text = subst.process(text)
    text = pywikibot.removeDisabledParts(text)
    text = pywikibot.removeLanguageLinks(text)
    text = pywikibot.removeCategoryLinks(text)
    text = pywikibot.removeHTMLParts(text)

    return text

def main():
    if "-html" not in args:
        return

    page = wp.Page(wp.toutf(raw_input()))
    dic = {}

    while True:
        if not page.exists():
            dic["error"] = u"ไม่มีหน้าดังกล่าว"
            break
        elif page.isRedirectPage():
            page = page.getRedirectTarget()
        else:
            try:
                oldtext = page.get()
            except:
                dic["error"] = u"เกิดข้อผิดพลาดไม่ทราบสาเหตุ"
            break

    if "error" not in dic:
        actuallen = lambda text: sum([int(32 < ord(i) < anchorBegin)
                                 for i in text])
        resgen = lambda x: "passed" if x else "failed"
        oldtext = lre.sub(r"[\t\r\f\v]", " ", oldtext)

        def placemarker(s):
            placemarker.i += 1
            return unichr((placemarker.i % (anchorEnd - anchorBegin + 1)) +
                          anchorBegin)

        placemarker.i = 0
        oldtext = lre.sub("(?m)^|$", placemarker, oldtext)
        oldtext = lre.sub(r"(?m)(?<=\|)(?=[^\[\]]*\]\])", placemarker, oldtext)
        oldtext = lre.sub(r"(?m)(?<=\])(?!\])", placemarker, oldtext)
        oldtext = lre.sub(r"(?m)(?<!\{)(?=\{)", placemarker, oldtext)
        oldtext = lre.sub(r"(?m)(?<=\})(?!\})", placemarker, oldtext)
        text = oldtext
        text, numinline0 = lre.subn(r"(?s)<ref[^>]*?/ *>", "", text)
        text, numinline = lre.subn(r"(?s)<ref.*?</ref>", "", text)
        numinline += numinline0
        dic["inline"] = {}
        dic["inline"]["value"] = (u"มีอ้างอิงในบรรทัดทั้งหมดจำนวน %d แห่ง" %
                                  numinline)
        dic["inline"]["result"] = "normal"
        dic["inline"]["text"] = u"อ้างอิง"
        text = rem(text)
        lentext = actuallen(text)
        dic["newtext"] = showdiff(oldtext, text)
        dic["len"] = {}
        dic["len"]["text"] = u"ความยาว"
        dic["len"]["result"] = resgen(lentext >= 2000)
        dic["len"]["value"] = u"%d อักขระ..." % lentext

        now = site.getcurrenttime()
        revid = None
        revtimestamp = None

        for rev in page.getVersionHistory(total=5000):
            ts = pywikibot.Timestamp.fromISOformat(rev[1])
            revid = rev[0]
            if (now - ts).days <= 14:
                revtimestamp = ts
            else:
                break

        dic["oldlen"] = {}
        dic["oldlen"]["text"] = u"รุ่นเก่า"

        if revtimestamp is None:
            dic["oldlen"]["result"] = resgen(False)
            dic["oldlen"]["value"] = u"ไม่พบรุ่นเก่าภายในเวลา 14 วัน"
        else:
            lenold = actuallen(rem(page.getOldVersion(revid)))
            dic["oldlen"]["result"] = resgen(
                                    (float(lentext)/float(lenold)) >= 3.0)
            dic["oldlen"]["value"] = (u"รุ่นเก่าก่อนการแก้ไขเมื่อ %s "
                                      u"(%d วันที่แล้ว) "
                                      u"มีความยาว %d อักขระ "
                                      u"จะได้ว่าขณะนี้มีเนื้อหาเป็น %.3f "
                                      u"เท่าเมื่อเทียบกับขณะนั้น..." %
                                (revtimestamp.strftime("%Y-%m-%d %H:%M:%S"),
                                (now - revtimestamp).days, lenold,
                                float(lentext)/float(lenold)))

        creator = page.getVersionHistory(reverseOrder=True, total=1)[0]
        tscreate = pywikibot.Timestamp.fromISOformat(creator[1])
        dic["create"] = {}
        dic["create"]["text"] = u"สร้างบทความ"
        dic["create"]["result"] = resgen((now - tscreate).days <= 14)
        dic["create"]["value"] = (u"บทความนี้สร้างโดย %s "
                                  u"เมื่อ %s (%d วันที่แล้ว)" % (creator[2],
                                  tscreate.strftime("%Y-%m-%d %H:%M:%S"),
                                  (now - tscreate).days))

        if ((dic["create"]["result"] == resgen(True)) or
                                        (dic["oldlen"]["result"] ==
                                        resgen(True))):
            if dic["create"]["result"] == resgen(False):
                dic["create"]["result"] = "normal"

            if dic["oldlen"]["result"] == resgen(False):
                dic["oldlen"]["result"] = "normal"

    print json.dumps(dic)

if __name__ == "__main__":
    args, site, conf = wp.pre("DYK Checker")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
