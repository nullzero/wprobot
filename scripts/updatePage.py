#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Update page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import sys
import time
import init
import wp
import pywikibot
from wp import lre, lnotify, lthread, ltime

debug = False

def glob():
    lre.pats["entry"] = lre.lre(ur"(?sm)\{\{\s*แจ้งปรับปรุงหน้าอัตโนมัติ\s*"
                                ur"((?:\{\{.*?\}\}|.)*?)\s*\}\}")
    lre.pats["param"] = lre.lre(r"(?s)\|\s*((?:\{\{.*?\}\}|.)*?)\s*(?=\|)")
    lre.pats["num"] = lre.lre(r"\d+$")
    lre.pats["user0"] = lre.lre(r"\{\{User0\|(.*?)\}\}")

def checkparams(params):
    # NotImplemented
    return True

def error(e, desc=None):
    # NotImplemented
    pywikibot.output("E: " + e)
    if desc:
        pywikibot.output(">>> " + desc)

def parse(text):
    if not (text[0] == '"' and text[-1] == '"'): error()
    return (text[1:-1].replace("\\\\", "<!-- B1acks1ash dummy -->\\"
                                       "<!-- B1acks1ash dummy -->")
                      .replace("\\{", "{")
                      .replace("\\}", "}")
                      .replace("\\!", "|")
                      .replace("\\n", "\n")
            ).replace("<!-- B1acks1ash dummy -->", "")

def process(text):
    params = {"find"  : [], "replace"   : [],
              "param" : [], "translate" : [],
              "depr"  : [], "rdepr"     : []}
    errorlist = []
    deprecated = []
    checkcat = []
    for param in lre.pats["param"].finditer(text + "|"):
        param = param.group(1)
        key, dat = param.split("=", 1)
        key = key.strip()
        dat = dat.strip()
        if key in conf.translateKey:
            params[conf.translateKey[key]] = dat
        else:
            key = lre.pats["num"].sub("", key)
            dat = lre.pats["num"].sub("", dat)
            if key in conf.seriesKey:
                params[conf.seriesKey[key]].append(dat)
            else:
                error("unknown parameter", param)

    if not checkparams(params):
        error("something wrong")
        return

    if "disable" in params and params["disable"] == conf.yes:
        return

    source = wp.Page(params["source"])
    page = wp.Page(params["page"])
    today = site.getcurrenttime()

    if ("stable" in params and (today - pywikibot.Timestamp.fromISOformat(
                    source.getVersionHistory(total=1)[0][1])).days <
                    int(params["stable"])):
        return

    params["notifyuser"] = [lre.pats["user0"].find(x.strip(), 1)
                            for x in params["notifyuser"].split("\n")]
    text = source.get()

    #=======

    for i, sfind in enumerate(params["find"]):
        newtext = text.replace(parse(sfind), parse(params["replace"][i]))
        if newtext == text:
            errorlist.append(u"คำเตือน: ไม่เกิดการแทนที่ข้อความที่ %d" %
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
            errorlist.append(u"คำเตือน: ไม่เกิดการแปลพารามิเตอร์ที่ %d" %
                            (irep + 1))
        text = newtext

    for i, sdepr in enumerate(params["depr"]):
        category = wp.Category("Category:" + page.title().replace(":", "") +
                               u"ที่ใช้พารามิเตอร์" + sdepr)
        checkcat.append(category)
        deprecated.append(u'<includeonly>{{#if:{{{%(depr)s|}}}|[[%(cat)s]]'
                          u'<span class="error">พารามิเตอร์ %(depr)s '
                          u'ล้าสมัยแล้ว โปรดใช้ %(rdepr)s แทนที่</span><br />'
                          u'}}</includeonly>'
            % {
                "depr": sdepr,
                "rdepr": params["rdepr"][i],
                "cat": category.title(),
            })
    text = "".join(deprecated) + text

    #=======

    if (not errorlist) and (text == page.get()):
        pywikibot.output(u"ไม่มีการเปลี่ยนแปลงในหน้า %s; "
                         u"ยกเลิกการปรับปรุงและแจ้งเตือน" % source.title())
        return

    if debug:
        pywikibot.showDiff(page.get(), text)
        return

    if "sandbox" in params and params["sandbox"] == conf.yes:
        page = wp.Page(page.title() + "/sandbox")

    page.put(text, u"ปรับปรุงหน้าอัตโนมัติโดยบอต")

    if checkcat:
        time.sleep(30)
        for cat in checkcat:
            if cat.isEmptyCategory():
                errorlist.append(u"[[:%s]] ว่างลงแล้ว "
                                 u"แสดงว่าไม่มีพารามิเตอร์ล้าสมัย "
                                 u"คุณอาจเขียนคู่มือการใช้งานใหม่"
                                 u"และลบการตั้งค่าพารามิเตอร์ล้าสมัยออก" %
                                 cat.title())

    for user in params["notifyuser"]:
        lnotify.notify("updatePage", wp.User(user).getUserTalkPage(), {
                    "page": page.title(),
                    "error": "".join(map(lambda x: "* " + x + "\n", errorlist)),
                    "warn_module": u"และดู [[:หมวดหมู่:หน้าที่มีสคริปต์ผิดพลาด]] " if
                                   page.namespace() == 828 else ""
                }, u"แจ้งการปรับปรุงหน้าอัตโนมัติ")

def process0(text):
    try:
        process(text)
    except:
        wp.error()

def main():
    pool = lthread.ThreadPool(30)
    for req in lre.pats["entry"].finditer(wp.Page(conf.title).get()):
        pool.add_task(process, req.group(1))
    pool.wait_completion()

if __name__ == "__main__":
    args, site, conf = wp.pre("updatePage")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
