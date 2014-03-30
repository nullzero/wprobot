#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Fill label!"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import itertools
import init
import wp
import pywikibot
from wp import lre
from pywikibot.tools import itergroup

def glob():
    lre.pats["rmdisam"] = lre.lre(ur"\s+\([^\(]*?\)\s*$")
    lre.pats["thai"] = lre.lre(u"[\u0e00-\u0e7f]")
    lre.pats["exc"] = lre.lre("(?m)^\* *\[\[ *(.*?) *\]\] *$")

def transform(dic):
    out = {}
    for i in dic:
        out[i] = {"th": {"language": "th", "value": dic[i]}}
    return out

def main():
    exlist = [exc.group(1) for exc in
              lre.pats["exc"].finditer(
              wp.Page(conf.pageConf).get())]
    pages1, pages2, pages3 = [], [], []
    if not args:
        pywikibot.output("quickscan mode")
        t = site.getcurrenttime()
        if t.day == 1:
            if t.month == 1:
                t = pywikibot.Timestamp(year=t.year-1, month=12, day=31)
            else:
                t = pywikibot.Timestamp(year=t.year, month=t.month-1, day=28)
        else:
            t = pywikibot.Timestamp(year=t.year, month=t.month, day=t.day-1)

        gen1 = site.recentchanges(start=t, reverse=True, showRedirects=False,
                                  showBot=False, changetype=["new", "edit"],
                                  namespaces=conf.namespaces)
        pages1 = [page["title"] for page in gen1]
        gen2 = site.logevents(start=t, reverse=True, logtype="move")
        pages2 = [page.new_title().title() for page in gen2]
    elif args[0] == "-all":
        pywikibot.output("fullscan mode")
        gen3 = ()
        for i in conf.namespaces:
            gen3 = itertools.chain(gen3, site.allpages(filterredir=False,
                                                       start=u"ก",
                                                       namespace=i))
        pages3 = [page.title() for page in gen3]
        pywikibot.output("load all!")
    else:
        pages1 = [u"หมวดหมู่:ชาววิกิพีเดียรักองค์โสมฯ"]
        pywikibot.output("unknown argument")

    allpages = list(set(filter(lambda x: (ord(u"ก") <= ord(x[0]) <= ord(u"๛")),
               pages1 + pages2 + pages3)))
    datasite = site.data_repository()
    cnti = 0
    pywikibot.output("processing %d pages" % len(allpages))

    for check in conf.checklist:
        if check["detectFromTitle"] is None: check["detectFromTitle"] = "[]" # dummy string which invalid for title
        for checkClaim in check["claims"]:
            checkClaim["nameItem"] = pywikibot.ItemPage(datasite, checkClaim["nameItem"])
            if checkClaim["refItem"] is not None:
                checkClaim["refItem"] = pywikibot.ItemPage(datasite, checkClaim["refItem"])

    for pages in itergroup(allpages, 100):
        cnti += 1
        pywikibot.output("round %d" % cnti)
        dat = datasite.loadcontent({"sites": site.dbName(),
                                    "titles": "|".join(pages)})
        for i, qitem in enumerate(dat):
            pywikibot.output("item %d: %s" % (i, qitem))
            if not qitem.lower().startswith("q"): continue
            item = pywikibot.ItemPage(datasite, qitem)
            item._content = dat[qitem]
            super(pywikibot.ItemPage, item).get() # For getting labels
            data = item.get()
            editdict = {}
            page = wp.Page(item.getSitelink(site))
            if page.title() in exlist: continue
            for check in conf.checklist:
                passCriteria = False
                description = None
                if check["detectFromTitle"] in page.title(): passCriteria = True
                if check["detectFromNamespace"] == page.namespace(): passCriteria = True
                passAlItem = True
                for claimCheck in check["claims"]:
                    passItem = False
                    if claimCheck["name"] in data["claims"]:
                        for claim in data["claims"][claimCheck["name"]]:
                            if claim.getTarget() == claimCheck["nameItem"]:
                                passItem = True
                                break

                    if not passItem:
                        passAllItem = False
                        if passCriteria:
                            claim = pywikibot.Claim(datasite, claimCheck["name"])
                            claim.setTarget(claimCheck["nameItem"])
                            item.addClaim(claim)
                            if claimCheck["ref"] is not None:
                                claim2 = pywikibot.Claim(datasite, claimCheck["ref"])
                                claim2.setTarget(claimCheck["refItem"])
                                claim.addSource(claim2)
                            pywikibot.output("added claim!")
                passCriteria = passCriteria or passAllItem
                if (description is None) and passCriteria:
                    description = check["description"]
                if passCriteria: break

            oldlabels = None
            if "th" in data["labels"]:
                oldlabels = data["labels"]["th"]
            labels = lre.pats["rmdisam"].sub("", page.title())
            if not lre.pats["thai"].search(labels): continue
            if labels != oldlabels:
                pywikibot.output("old label: " + unicode(oldlabels))
                pywikibot.output("new label: " + unicode(labels))
                editdict["labels"] = labels
            if passCriteria and (("th" in data["descriptions"] and
                            data["descriptions"]["th"] != description) or
                            ("th" not in data["descriptions"])):
                editdict["descriptions"] = description
            out = transform(editdict)
            if not out:
                continue
            pywikibot.output("item: " + qitem)
            pywikibot.output("title: " + page.title())
            try:
                #raw_input("prompt: ...")
                item.editEntity(out)
            except:
                wp.error()
                pass

args, site, conf = wp.pre(4, lock=True, main=__name__)
try:
    glob()
    wp.run(main)
except:
    wp.posterror()
else:
    wp.post()
