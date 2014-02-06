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
    global putWithSysop
    lre.pats["entry"] = lre.lre(ur"(?sm)\{\{\s*แจ้งปรับปรุงหน้าอัตโนมัติ\s*"
                                ur"((?:\{\{.*?\}\}|.)*?)\s*\}\}")
    lre.pats["param"] = lre.lre(r"(?s)\|\s*((?:\{\{.*?\}\}|.)*?)\s*(?=\|)")
    lre.pats["num"] = lre.lre(r"\d+$")
    lre.pats["user0"] = lre.lre(r"\{\{User0\|(.*?)\}\}")
    lre.pats["trimComment"] = lre.lre(r"<!--#(.*?)#-->")
    putWithSysop = []

def checkparams(params):
    # NotImplemented
    return True

def error(e, desc=None):
    # NotImplemented
    pywikibot.output("E: " + e)
    if desc:
        pywikibot.output(">>> " + unicode(desc))

def parse(text):
    if not (text[0] == '"' and text[-1] == '"'):
        error("not begin or end with double quote", text)
        sys.exit()
    return lre.pats["trimComment"].sub("", 
            (text[1:-1].replace("\\\\", "<!--##-->\\<!--##-->")
                        .replace("\\{", "{")
                        .replace("\\}", "}")
                        .replace("\\!", "|")
                        .replace("\\n", "\n")))

def process(text, page_config):
    global putWithSysop

    params = {}
    for key in conf.seriesKey:
        params[conf.seriesKey[key]] = []

    errorlist = []
    deprecated = []
    checkcat = []
    try:
        for param in lre.pats["param"].finditer(text + "|"):
            param = param.group(1)
            key, dat = param.split("=", 1)
            key = key.strip()
            dat = dat.strip()
            if key in conf.translateKey:
                params[conf.translateKey[key]] = dat
            else:
                num = lre.pats["num"].find(key)
                key = lre.pats["num"].sub("", key)
                if key in conf.seriesKey:
                    params[conf.seriesKey[key]].append((num, dat))
                else:
                    error("unknown parameter", param)
    except:
        wp.error()
        if "source" in params:
            pywikibot.output(u"Error when updating %s" % params["source"])
        else:
            pywikibot.output(u"Error when processing page %s" % page_config)
        return

    if not checkparams(params):
        error("something wrong")
        return

    if "disable" in params and params["disable"] == conf.yes:
        return

    source = wp.Page(params["source"])
    page = wp.Page(params["page"])
    today = site.getcurrenttime()
    originalText = page.get() if page.exists() else None

    if ("stable" in params and (today - pywikibot.Timestamp.fromISOformat(
                    source.getVersionHistory(total=1)[0][1])).days <
                    int(params["stable"])):
        return

    params["notifyuser"] = [lre.pats["user0"].find(x.strip(), 1)
                            for x in params["notifyuser"].split("\n")]
    text = source.get()

    #=======

    for i, (num, sfind) in enumerate(params["find"]):
        newtext = text.replace(parse(sfind), parse(params["replace"][i][1]))
        if newtext == text and sfind != params["replace"][i][1]:
            errorlist.append(u"คำเตือน: ไม่เกิดการแทนที่ข้อความที่ {0}".format(num))
        text = newtext

    def matchbrace(s, i):
        lv = 0
        for i in xrange(i, len(s)):
            if s[i] == "{": lv += 1
            elif s[i] == "}": lv -= 1
            if lv == 0:
                return i
                # not return i + 1 to avoid index out of range

    for irep, (num, sp) in enumerate(params["param"]):
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
                    out.append("{{{" + params["translate"][irep][1] + "|")
                else:
                    out.append("}}}")
                    # we should put text[i] before "}}}",
                    # but since text[i] == "}", there is no problem :)
                ilst += 1
            out.append(text[i])
        newtext = "".join(out)
        if newtext == text:
            errorlist.append(u"คำเตือน: ไม่เกิดการแปลพารามิเตอร์ที่ {0}".format(num))
        text = newtext

    for i, (num, sdepr) in enumerate(params["depr"]):
        category = wp.Category("Category:" + page.title().replace(":", "") +
                               u" ที่ใช้พารามิเตอร์ " + sdepr)
        checkcat.append(category)
        deprecated.append(u'<includeonly>{{{{#if:{{{{{{{depr}|}}}}}}|[[{cat}]]'
                          .format(depr=sdepr, cat=category.title()) +            
                          ((u'<span class="error">พารามิเตอร์ {depr} '
                          u'ล้าสมัยแล้ว โปรดใช้ {rdepr} แทนที่</span><br />')
                          .format(depr=sdepr, rdepr=params["rdepr"][i][1])
                          if (params["errordepr"][i][1] == conf.yes) else u'') +
                          u'}}</includeonly>')
    text = "".join(deprecated) + text

    #=======

    if (not errorlist) and (text == originalText):
        pywikibot.output(u"ไม่มีการเปลี่ยนแปลงในหน้า %s; "
                         u"ยกเลิกการปรับปรุงและแจ้งเตือน" % source.title())
        return

    if debug:
        pywikibot.showDiff(originalText or "", text)
        return

    if "sandbox" in params and params["sandbox"] == conf.yes:
        page = wp.Page(page.title() + "/sandbox")

    try:
        page.put(text, u"ปรับปรุงหน้าอัตโนมัติโดยบอต")
    except (pywikibot.LockedPage, pywikibot.PageNotSaved):
        putWithSysop.append((page, text))
    except:
        wp.error()
        pywikibot.output("<!-- Begin error -->")
        pywikibot.output(text)
        pywikibot.output("<!-- End error -->")

    if checkcat:
        time.sleep(30)
        for cat in checkcat:
            if cat.isEmptyCategory():
                errorlist.append(u"[[:%s]] ว่างลงแล้ว "
                                 u"แสดงว่าไม่มีพารามิเตอร์ล้าสมัย "
                                 u"คุณอาจเขียนคู่มือการใช้งานใหม่"
                                 u"และลบการตั้งค่าพารามิเตอร์ล้าสมัยออก" %
                                 cat.title())

    #for user in params["notifyuser"]:
    for user in ["Nullzero"]:
        lnotify.notify("updatePage", wp.User(user).getUserTalkPage(), {
                    "page": page.title(),
                    "error": "".join(map(lambda x: "* " + x + "\n", errorlist)),
                    "warn_module": u"และดู [[:หมวดหมู่:หน้าที่มีสคริปต์ผิดพลาด]] " if # มีเดียวิกิ:Scribunto-common-error-category
                                   page.namespace() == 828 else "",
                    "page_config": page_config
                }, u"แจ้งการปรับปรุงหน้าอัตโนมัติ")

def main():
    pool = lthread.ThreadPool(30)
    gen = []
    page = wp.handlearg("page", args)
    if page is not None:
        gen = [wp.Page(page)]
    else:
        gen = site.allpages(prefix=conf.title, content=True, namespace=2)
    for page in gen:
        for req in lre.pats["entry"].finditer(page.get()):
            pool.add_task(process, req.group(1), page.title())
    pool.wait_completion()

    site.switchuser("Nullzero", False)
    for (page, text) in putWithSysop:
        try:
            page.put(text, u"ปรับปรุงหน้าอัตโนมัติโดยบอต")
        except:
            wp.error()
            pywikibot.output("<!-- Begin error -->")
            pywikibot.output(text)
            pywikibot.output("<!-- End error -->")

if __name__ == "__main__":
    args, site, conf = wp.pre(-2, lock=True)
    try:
        glob()
        wp.run(main)
    except:
        wp.posterror()
    else:
        wp.post()
