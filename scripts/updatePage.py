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
    lre.pats["trimComment"] = lre.lre(r"<!--#(.*?)#-->")

def error(e, desc=None):
    # NotImplemented
    pywikibot.output("E: " + e)
    if desc:
        pywikibot.output(">>> " + unicode(desc))

def parse(text):
    return lre.pats["trimComment"].sub("", text)

def callback(page, err):
    if isinstance(err, pywikibot.LockedPage) or isinstance(err, pywikibot.PageNotSaved):
        if hasattr(page, 'u_nomore'):
            page.u_err = True
        else:
            page.u_nomore = True
            page.put(page.u_text, u"ปรับปรุงหน้าอัตโนมัติโดยบอต", as_group='sysop', async=True)
            return
    elif err:
        page.u_err = True
    
    if hasattr(page, 'u_err'):
        pywikibot.output("<!-- Begin error -->")
        pywikibot.output(page.text)
        pywikibot.output("<!-- End error -->")
        page.u_elist.append(u"ผิดพลาด: ไม่เกิดการเขียนหน้า <pre>{}</pre>".format(sys.exc_info()[0]))
        wp.error()
        return
        
    if page.u_checkcat:
        time.sleep(30)
        for cat in page.u_checkcat:
            if cat.isEmptyCategory():
                page.u_elist.append((u"[[:{}]] ว่างลงแล้ว "
                                     u"แสดงว่าไม่มีพารามิเตอร์ล้าสมัย "
                                     u"คุณอาจเขียนคู่มือการใช้งานใหม่"
                                     u"และลบการตั้งค่าพารามิเตอร์ล้าสมัยออก").format(cat.title()))

    #for user in config["notifyuser"]:
    for user in ["Nullzero"]:
        lnotify.notify("updatePage", wp.User(user).getUserTalkPage(), {
                    "page": page.title(),
                    "error": "".join(map(lambda x: "* " + x + "\n", page.u_elist)),
                    "warn_module": u"และดู [[:หมวดหมู่:หน้าที่มีสคริปต์ผิดพลาด]] " if # มีเดียวิกิ:Scribunto-common-error-category
                                   page.namespace() == 828 else "",
                    "page_config": conf.title,
                    "revision": page.latestRevision(),
                }, u"แจ้งการปรับปรุงหน้าอัตโนมัติ")

def process(page, config):
    if config.get('disable', False): return
    
    source = wp.Page(config["source"])
    today = site.getcurrenttime()
    originalText = page.get() if page.exists() else None

    if ("stable" in config and (today - pywikibot.Timestamp.fromISOformat(
                    source.getVersionHistory(total=1)[0][1])).days <
                    int(config["stable"])):
        return
        
    page.u_elist = []
    deprecated = []
    checkcat = []

    text = source.get()

    #=======

    for item in config["findText"]:
        if len(item) == 3:
            num, find, replace = item
            regex = False
        elif len(item) == 4:
            num, find, replace, regex = item
        else:
            page.u_elist.append(u"คำเตือน: ข้อความค้นหาและแทนที่อันดับที่ {} มีจำนวนพารามิเตอร์ไม่ถูกต้อง".format(num))
            continue
        
        if regex:
            newtext = lre.sub(find, replace, text)
        else:
            newtext = text.replace(find, replace)
        if newtext == text and find != replace:
            page.u_elist.append(u"คำเตือน: ไม่เกิดการแทนที่ข้อความที่ {}".format(num))
        text = newtext

    def matchbrace(s, i):
        lv = 0
        for i in xrange(i, len(s)):
            if s[i] == "{": lv += 1
            elif s[i] == "}": lv -= 1
            if lv == 0:
                return i
                # not return i + 1 to avoid index out of range

    for item in config["addParam"]:
        if len(item) == 3:
            num, param, translate = item
        else:
            page.u_elist.append(u"คำเตือน: ข้อความแปลที่ {} มีจำนวนพารามิเตอร์ไม่ถูกต้อง".format(num))
            continue

        lst = []
        for i in lre.finditer(r"\{\{\{\s*" + param + "\s*[\|\}]", text):
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
                    out.append("{{{" + translate + "|")
                else:
                    out.append("}}}")
                    # we should put text[i] before "}}}",
                    # but since text[i] == "}", there is no problem :)
                ilst += 1
            out.append(text[i])
        newtext = "".join(out)
        if newtext == text:
            errorlist.append(u"คำเตือน: ไม่เกิดการแปลพารามิเตอร์ที่ {}".format(num))
        text = newtext
    
    for item in config["obsolete"]:
        if len(item) == 3:
            num, oldParam, newParam = item
            showError = False
        elif len(item) == 4:
            num, oldParam, newParam, showError = item
        else:
            page.u_elist.append(u"คำเตือน: การตรวจสอบพารามิเตอร์ล้าสมัยที่ {} มีจำนวนพารามิเตอร์ไม่ถูกต้อง".format(num))
            continue
            
        category = wp.Category("Category:" + page.title().replace(":", "") +
                               u" ที่ใช้พารามิเตอร์ " + oldParam)
        checkcat.append(category)
        deprecated.append(u'<includeonly>{{{{#if:{{{{{{{}|}}}}}}|[[{}]]'
                          .format(oldParam, category.title()) +            
                          ((u'<span class="error">พารามิเตอร์ {} '
                          u'ล้าสมัยแล้ว โปรดใช้ {} แทนที่</span><br />')
                          .format(oldParam, newParam)
                          if showError else u'') +
                          u'}}</includeonly>')
    text = "".join(deprecated) + text

    #=======
    if (not page.u_elist) and (text == originalText):
        pywikibot.output((u"ไม่มีการเปลี่ยนแปลงในหน้า {}; "
                          u"ยกเลิกการปรับปรุงและแจ้งเตือน").format(source.title()))
        return
    
    if debug:
        pywikibot.showDiff(originalText or "", text)
        return

    if config.get("sandbox", False):
        page = wp.Page(page.title() + "/sandbox")
    
    page.u_text = text
    page.put(text, u"ปรับปรุงหน้าอัตโนมัติโดยบอต", async=True, callback=callback)
        
def main():
    config = wp.ReadCode(wp.Page(conf.title), "config")
    config.load()
    config = config.data
    updateList = [wp.handlearg("page", args)]
    if not updateList[0]:
        updateList = config.keys()
    for title in updateList:
        page = wp.Page(title)
        process(page, config[page.title()]) # normalize page's name

args, site, conf = wp.pre(-2, main=__name__, lock=True)
try:
    glob()
    wp.run(main)
except:
    wp.posterror()
else:
    wp.post()
