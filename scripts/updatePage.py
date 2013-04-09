# -*- coding: utf-8  -*-
"""Update page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import sys
import init
import wp
import pywikibot
from wp import lre

debug = False

def glob():
    global translateKey, textnotify
    lre.pats["entry"] = lre.lre(ur"(?s)\{\{\s*แจ้งปรับปรุงหน้าอัตโนมัติ\s*(.*?)\s*\}\}")
    lre.pats["param"] = lre.lre(r"\s*\|([^\|]*?)\s*(?=\|)")
    lre.pats[""] = lre.lre(r"\n")

    translateKey = {}
    translateKey[u"หน้า"] = "page"
    translateKey[u"ต้นทาง"] = "source"
    translateKey[u"แจ้ง"] = "notifyuser"
    translateKey[u"กระบะทราย"] = "sandbox"
    translateKey[u"พัก"] = "disable"

    textnotify = (u"""== แจ้งการปรับปรุงหน้า [[%(page)s]] อัตโนมัติโดยบอต ==
บอตได้ทำการปรับปรุงหน้า [[%(page)s]] เรียบร้อยแล้ว """
u"([{{fullurl:%(page)s|diff=cur&oldid=prev}} ดูการแก้ไข]) "
u"โปรดตรวจสอบความถูกต้องของหน้าด้วย")

def checkparams(params):
    # NotImplemented
    return True

def error(e, desc=None):
    # NotImplemented
    print "E:", e
    if desc: print ">>> ", desc

def parse(text):
    if not (text[0] == '"' and text[-1] == '"'): error()
    return (text[1:-1].replace("\\\\", "<!-- B1acks1ash dummy -->\\"
                                       "<!-- B1acks1ash dummy -->")
                      .replace('\\"', '"')
                      .replace("\\{", "{")
                      .replace("\\}", "}")
                      .replace("\\!", "|")
                      .replace("\\n", "\n")
            ).replace("<!-- B1acks1ash dummy -->", "")

def process(text):
    params = {"find": [], "replace": [], "param": [], "translate": []}
    errorlist = []
    for param in lre.pats["param"].finditer(text + "|"):
        param = param.group(1)
        pywikibot.output(param)
        key, dat = param.split("=", 1)
        key = key.strip()
        dat = dat.strip()
        if key in translateKey:
            params[translateKey[key]] = dat
        elif key.startswith(conf.find):
            params["find"].append(dat)
        elif key.startswith(conf.replace):
            params["replace"].append(dat)
        elif key.startswith(conf.param):
            params["param"].append(dat)
        elif key.startswith(conf.translate):
            params["translate"].append(dat)
        else:
            error("unknown parameter", param)

    if not checkparams(params):
        error("something wrong")
        return

    if "disable" in params:
        return

    page = wp.Page(params["page"])
    source = wp.Page(params["source"])
    text = source.get()

    #=======

    for i, sfind in enumerate(params["find"]):
        newtext = text.replace(parse(sfind), parse(params["replace"][i]))
        if newtext == text:
            errorlist.append("คำเตือน: ไม่เกิดการแทนที่ข้อความที่ %d" %
                            (i + 1))
        text = newtext

    def matchbrace(s, i):
        lv = 0
        for i in xrange(i, len(s)):
            if s[i] == "{": lv += 1
            elif s[i] == "}": lv -= 1
            if lv == 0:
                return i
                # not return i + 1 to avoid index out of range

    for irep, sp in enumerate(params["param"]):
        lst = []
        for i in lre.finditer(r"\{\{\{\s*" + sp + "\s*[\|\}]", text):
            begin, end = i.span()
            end = matchbrace(text, begin)
            lst.append((begin, "begin"))
            lst.append((end, "end"))
        lst = sorted(lst)
        lst.append((sys.maxint, sys.maxint))
        ilst = 0
        out = []
        for i in xrange(len(text)):
            if i == lst[ilst][0]:
                if lst[ilst][1] == "begin":
                    out.append("{{{" + params["translate"][irep] + "|")
                else:
                    out.append("}}}")
                    # we should put text[i] before "}}}",
                    # but since text[i] == "}", there is no problem :)
                ilst += 1
            out.append(text[i])
        newtext = "".join(out)
        if newtext == text:
            errorlist.append("คำเตือน: ไม่เกิดการแปลพารามิเตอร์ที่ %d" %
                            (irep + 1))
        text = newtext

    #=======

    if text == page.get():
        pywikibot.output(u"ไม่มีการเปลี่ยนแปลงในหน้า %s; "
                         u"ยกเลิกการปรับปรุงและแจ้งเตือน" % source.title())
        return

    if debug:
        pywikibot.showDiff(page.get(), text)
        return

    global textnotify
    textnotify += "\n" + "".join(map(lambda x: "* " + x + "\n", errorlist))

    if "sandbox" in params:
        page = wp.Page(page.title() + "/sandbox")

    page.put(text, u"ปรับปรุงหน้าอัตโนมัติโดยบอต")
    pagenotify = wp.User(params["notifyuser"]).getUserTalkPage()
    pagenotify.put(pagenotify.get() + "\n\n" + textnotify % {
                                                "page": page.title(),
                                            } + "--~~~~",
                   u"แจ้งการปรับปรุงหน้าอัตโนมัติ", minorEdit=False)

def main():
    text = wp.Page(u"ผู้ใช้:Nullzerobot/ปรับปรุงหน้าอัตโนมัติ").get()
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
