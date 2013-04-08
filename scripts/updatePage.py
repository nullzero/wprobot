# -*- coding: utf-8  -*-
"""Update page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from wp import lre

def glob():
    global translateKey
    lre.pats["entry"] = lre.lre(ur"(?s)\{\{\s*ปรับปรุงหน้าอัตโนมัติ\s*(.*?)\s*\}\}")
    lre.pats["param"] = lre.lre(r"\s*\|([^\|]*?)\s*(?=\|)")
    
    translateKey = {}
    translateKey[u"หน้า"] = "page"
    translateKey[u"ต้นทาง"] = "source"
    translateKey[u"แจ้ง"] = "notify"

def checkparams(params):
    return True

def error():
    pass

def process(text):
    params = {}
    for param in lre.pats["param"].finditer(text + "|"):
        param = param.group(1)
        key, dat = param.split("=", 1)
        key = key.strip()
        dat = dat.strip()
        if key in translateKey:
            params[translateKey[key]] = dat
        else:
            error()
    
    if not checkparams(params):
        error()
        return
    
    page = wp.Page(params["page"])
    source = wp.Page(params["source"])
    

def main():
    page = wp.Page(u"ผู้ใช้:Nullzerobot/ปรับปรุงหน้าอัตโนมัติ")
    text = page.get().replace("{{!}}", "<!-- p1p3 dummy -->")
    for req in lre.pats["entry"].finditer(text):
        process(req.group(1))

        
if __name__ == "__main__":
    args, site, conf = wp.pre("updatePage")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
