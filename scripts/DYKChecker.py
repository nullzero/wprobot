# -*- coding: utf-8  -*-
"""DYKChecker!"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import json
import init
import wp
import pywikibot
from wp import lre

def glob():
    pass

def main():
    page = wp.Page(wp.toutf(raw_input()))
    dic = {}
    
    while True:
        try:
            text = page.get()
            break
        except pywikibot.NoPage:
            dic["error"] = u"ไม่มีหน้าดังกล่าว"
            break
        except pywikibot.IsRedirectPage:
            page = page.getRedirectTarget()
        except:
            dic["error"] = u"เกิดข้อผิดพลาดไม่ทราบสาเหตุ"
            break
    
    oldtext = text
    
    if "error" not in dic:
        # delete all references
        text, numinline = lre.subn(r"(?s)<ref.*?</ref>", "", text)
        text = lre.rmsym(r"\{\{", r"\}\}", text)
        text = lre.rmsym(r"\{\|", r"\|\}", text)
        text = pywikibot.removeDisabledParts(text)
        text = pywikibot.removeHTMLParts(text)
        text = pywikibot.removeLanguageLinks(text)
        text = pywikibot.removeCategoryLinks(text)
        
        subst = lre.subst()
        subst.append((r"[ \t]+", " "))
        subst.append((r"(\n{2})\n*", r"\1"))
        subst.append((r"(?s)(?<!\[)\[(?!\[).*?\]", ""))
        subst.append((r"[\[\]]", ""))
        
        text = subst.process(text)
        
        dic["newtext"] = text
        dic["len"] = {}
        dic["len"]["value"] = len(text)
        dic["len"]["result"] = "passed" if (dic["len"]["value"] >= 2000) else "failed"
    
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
