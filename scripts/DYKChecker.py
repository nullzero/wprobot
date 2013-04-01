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
    pass

def showdiff(a, b):
    out = []
    match = False
    i, j = 0, 0
    while i < len(a) and j < len(b):
        if match != (a[i] == b[j]):
            match = not match
            out.append("~~~OPENSESAME~~~" if match else "~~~CLOSESESAME~~~")
        out.append(a[i])
        i += 1
        j += int(match)
        
    return "".join(out + ["~~~CLOSESESAME~~~" if match else ""] + list(a[i:]))

def rem(text):
    # delete table -- TODO: ^\{\{ or ^[\*\:\#]*\{\{
    text = lre.rmsym(r"\{\|", r"\|\}", text)
    
    # delete template
    text = lre.rmsym(r"\{\{", r"\}\}", text)
    
    
    subst = lre.subst()
    
    pywikibot.output("1234")
    # delete inline ref
    subst.append((r"(?s)<ref[^>]*?/\s*>", ""))
    subst.append((r"(?s)<ref.*?</ref>", ""))
    
    # delete external links
    subst.append((r"(?s)(?<!\[)\[(?!\[).*?\]", ""))
    subst.append((r"http://\S*", ""))
    
    # delete gallery
    subst.append((r"(?is)<gallery.*?>.*?</gallery>", ""))
    
    # delete non article links, must be called before deleting links
    subst.append((r"(?is)\[\[[^\]\|]*?\:.*?\]\]", ""))
    
    # delete links
    subst.append((r"[\[\]]", ""))
    
    # delete other markup
    subst.append(("\'{2,}", ""))
    
    # delete header
    subst.append((r"(?m)^\=+.*?\=+ *$", ""))
    
    # delete list
    subst.append((r"(?m)^[\:\*\#]*", ""))
    
    
    #-------
    # delete consecutive space, this subst should be called last.
    subst.append((r" +", " "))
    
    # delete many newlines, this subst should be called last.
    subst.append((r"(\n{2})\n*", r"\1"))
    #-------
    
    text = subst.process(text)
    
    text = pywikibot.removeDisabledParts(text)
    text = pywikibot.removeLanguageLinks(text)
    text = pywikibot.removeCategoryLinks(text)
    text = pywikibot.removeHTMLParts(text)
    
    return text

def main():
    page = wp.Page(wp.toutf(raw_input()))
    dic = {}
    
    while True:
        try:
            oldtext = page.get()
            break
        except pywikibot.NoPage:
            dic["error"] = u"ไม่มีหน้าดังกล่าว"
            break
        except pywikibot.IsRedirectPage:
            page = page.getRedirectTarget()
        except:
            dic["error"] = u"เกิดข้อผิดพลาดไม่ทราบสาเหตุ"
            break
    
    if "error" not in dic:
        resgen = lambda x: "passed" if x else "failed"
        dateDistance = lambda x,y: ((time.mktime(y.timetuple()) -
                       time.mktime(x.timetuple())) // (60 * 60 * 24))
        
        oldtext = lre.sub(r"[\t\r\f\v]", " ", oldtext)
        text = oldtext
        text, numinline0 = lre.subn(r"(?s)<ref[^>]*?/\s*>", "", text)
        text, numinline = lre.subn(r"(?s)<ref.*?</ref>", "", text)
        numinline += numinline0
        dic["inline"] = {}
        dic["inline"]["value"] = (u"มีอ้างอิงในบรรทัดทั้งหมดจำนวน %d แห่ง" % 
                                  numinline)
        dic["inline"]["result"] = "normal"
        dic["inline"]["text"] = u"อ้างอิง"
        text = rem(text)
        #dic["dtext"] = text
        dic["newtext"] = showdiff(oldtext, text)
        dic["len"] = {}
        dic["len"]["text"] = u"ความยาว"
        dic["len"]["result"] = resgen(len(text) >= 2000)
        dic["len"]["value"] = u"%d อักขระ..." % len(text)
        
        now = site.getcurrenttime()
        revid = None
        
        for rev in page.getVersionHistory(total=5000):
            ts = pywikibot.Timestamp.fromISOformat(rev[1])
            if dateDistance(ts, now) <= 14:
                revid = rev[0]
                revtimestamp = ts
        
        dic["oldlen"] = {}
        dic["oldlen"]["text"] = u"รุ่นเก่า"
        
        if revid is None:
            dic["oldlen"]["result"] = resgen(False)
            dic["oldlen"]["value"] = u"ไม่พบรุ่นเก่าภายในเวลา 14 วัน"
        else:
            lenold = len(rem(page.getOldVersion(revid)))
            dic["oldlen"]["result"] = resgen(
                                    (float(len(text))/float(lenold)) >= 3.0)
            dic["oldlen"]["value"] = (u"รุ่นเก่าเมื่อ %s มีความยาว %d อักขระ "
                                      u"จะได้ว่าขณะนี้มีเนื้อหาเป็น %.3f "
                                      u"เท่าเมื่อเทียบกับขณะนั้น..." % 
                                (revtimestamp.strftime("%Y-%m-%d %H:%M:%S"),
                                      lenold, float(len(text))/float(lenold)))
        
        creator = page.getVersionHistory(reverseOrder=True, total=1)[0]
        tscreate = pywikibot.Timestamp.fromISOformat(creator[1])
        dic["create"] = {}
        dic["create"]["text"] = u"สร้างบทความ"
        dic["create"]["result"] = resgen(dateDistance(tscreate, now) <= 14)
        dic["create"]["value"] = u"บทความนี้สร้างโดย %s เมื่อ %s..." % (
                        creator[2], tscreate.strftime("%Y-%m-%d %H:%M:%S"))
                                 
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
