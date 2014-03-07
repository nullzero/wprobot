#!/usr/bin/python
# -*- coding: utf-8 -*-

import itertools
import init
import wp
import pywikibot
from wp import lre, lthread, lservice

def glob():
    global dummytext
    dummytext = "<!-- dummy -->"
    lre.pats["maintaincat"] = lre.lre("(?i)article|stub|wikipedia|without")
    lre.pats["name"] = lre.lre(r"\[\[:(.*?)\]\]")
    lre.pats["dummy"] = lre.lre(dummytext + r"\s*")

def subthread(pagep, catinp, cat, page):
    if not page:
        pywikibot.output(pagep.title() + " not found")
        return
    pywikibot.output("thread %s >>> adding..." % page.title())
    try:
        if page.namespace() not in wp.conf.nstl:
            oldcat = set(page.categories(fromtext=True))
            newcat = (oldcat - set([catinp])) | set([cat])
            if oldcat != newcat:
                pywikibot.output("Change!")
                text = pywikibot.replaceCategoryLinks(page.get(), list(newcat),
                                                      site)
                page.put(text, u"autoCategory")
            else:
                pywikibot.output("Nothing changes!")
    except:
        wp.error()

def doCategory(pool, cat, catp):
    if not cat:
        return
    if not catp:
        return
    pywikibot.output("processing: %s, %s" % (cat.title(), catp.title()))
    cat = pywikibot.Category(cat) # to ensure that it is a Category object
    catp = pywikibot.Category(catp)
    catinp = wp.Category(catp.title())
    if (cat.title(withNamespace=False) == catinp.title(withNamespace=False)):
        pywikibot.output("found English category: %s" %
                         catinp.title(withNamespace=False))
        return
    pagesp = filter(lambda x: x.namespace() in [0, 10, 14],
                    list(catp.articles(content=True)) +
                    list(catp.subcategories(content=True)))
    pages = site.getLang(pagesp)
    for i, pagep in enumerate(pagesp):
        pool.add_task(subthread, pagep, catinp, cat, pages[i])

def importiw(A, B):
    datapage = pywikibot.ItemPage.fromPage(A)
    if datapage.exists():
        pywikibot.output("something wrong")
        return

    langdic = {}
    sitedic = {}

    for page in list(A.langlinks()) + [A, B]:
        page = pywikibot.Page(page) # convert both Link and Page to Page
        vsite = page.site.dbName()
        vlang = page.site.lang
        vtitle = page.title()
        langdic[vlang] = {"language": vlang, "value": vtitle}
        sitedic[vsite] = {"site": vsite, "title": vtitle}

    datapage.editEntity({"labels": langdic, "sitelinks": sitedic})
    pywikibot.output("import done!")

def addItem(datapage, wikipage):
    vlang = wikipage.site.lang
    vtitle = wikipage.title()
    vsite = wikipage.site.dbName()
    data = {}
    langdic = {}
    sitedic = {}
    langdic[vlang] = {"language": vlang, "value": vtitle}
    sitedic[vsite] = {"site": vsite, "title": vtitle}
    datapage.editEntity({"sitelinks": sitedic, "labels": langdic})

def doall(title, titlep):
    global sitep
    pywikibot.output("autoCategory: %s, %s" % (title, titlep))
    page = wp.Page(title)
    if not titlep:
        pagep = page.getLang(pywikibot.Site("en"))
    else:
        pagep = wp.Page(titlep)

    sitep = pagep.site

    if page.exists():
        missingcats = set(page.categories(fromtext=True))
        oldtext = page.get()
    else:
        missingcats = set()
        oldtext = ""

    oldcats = set(missingcats)
    catsp = list(pagep.categories(fromtext=True))
    cats = site.getLang(catsp)

    for i, catp in enumerate(catsp):
        if not cats[i]:
            missingcats.add(wp.Category(catp.title()))

    if page.namespace() not in wp.conf.nstl:
        text = pywikibot.replaceCategoryLinks(oldtext, list(missingcats), site)
    else:
        return NotImplementedError

    if (oldcats != missingcats) or (text == ""):
        pywikibot.output(">>> add untranslated categories")
        page.put(text or dummytext, u"เพิ่มหมวดหมู่")

    data = pywikibot.ItemPage.fromPage(page)
    datap = pywikibot.ItemPage.fromPage(pagep)

    if (not data.exists()) and (not datap.exists()):
        importiw(pagep, page)
    elif not datap.exists():
        addItem(data, pagep)
    elif not data.exists():
        addItem(datap, page)
    elif data.getID() != datap.getID():
        return False

    pool = lthread.ThreadPool(10)

    if page.isCategory():
        doCategory(pool, page, pagep)

    for i, catp in enumerate(catsp):
        pywikibot.output(catp.title())
        if not lre.pats["maintaincat"].search(catp.title()) and cats[i]:
            page.add_category([cats[i]])
            #doCategory(pool, cats[i], catp)

    pool.wait_completion()

    text = lre.pats["dummy"].sub("", page.get())
    if page.get() != text:
        page.put(text, u"ลบข้อความ dummy")

    return True

def summaryWithTime():
    return u"บอตจัดหมวดหมู่และลิงก์ข้ามภาษา (วิกิสนเทศ) อัตโนมัติ @ %s" % wp.getTime()

def main():
    title = u"ผู้ใช้:Nullzerobot/บริการจัดหมวดหมู่/หมวดหมู่ที่รอการจัด"
    confpage = u"ผู้ใช้:Nullzerobot/บริการจัดหมวดหมู่/"
    header, table, disable = lservice.service(page=wp.Page(title),
                                              confpage=wp.Page(confpage),
                                              operation="major",
                                              verify=lambda x: True,
                                              summary=summaryWithTime,
                                              #debug=True,
                                              )

    for line in table:
        try:
            doall(lre.pats["name"].find(line[1], 1),
                  lre.pats["name"].find(line[2], 1))
        except:
            wp.error()

args, site, conf = wp.pre(-3, lock=True, main=__name__)
try:
    glob()
    wp.run(main)
except:
    wp.posterror()
else:
    wp.post()
