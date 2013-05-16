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
              wp.Page(u"ผู้ใช้:Nullzerobot/ปรับปรุงชื่อฉลาก").get())]
    t = site.getcurrenttime()
    t = pywikibot.Timestamp(year=t.year, month=t.month, day=t.day - 1)
    gen = site.recentchanges(start=t, reverse=True, showRedirects=False,
                             namespaces=[0, 4, 10, 14])
    datasite = site.data_repository()
    disamitem = pywikibot.ItemPage(datasite, "Q11651459")
    thwikiitem = pywikibot.ItemPage(datasite, "Q565074")
    wrongdisamitem = pywikibot.ItemPage(datasite, "Q4167410")
    descdisam = u"หน้าแก้ความกำกวมวิกิพีเดีย"
    for pages in itergroup(gen, 100):
        pages = [wp.Page(page["title"]) for page in pages if
                 ord(u"ก") <= ord(page["title"][0]) <= ord(u"๛")]
                 # not block other namespace
        dat = datasite.loadcontent({"sites": site.dbName(),
                                    "titles": "|".join([page.title()
                                                        for page in pages])})

        for i, qitem in enumerate(dat):
            if not qitem.startswith("q"): continue
            item = pywikibot.ItemPage(datasite, qitem)
            item._content = dat[qitem]
            super(pywikibot.ItemPage, item).get() # For getting labels
            data = item.get()
            editdict = {}
            isdisam = False
            isdisamtitle = False
            wrongdisam = None
            page = wp.Page(item.getSitelink(site))
            if page.title() in exlist:
                continue
            if u"(แก้ความกำกวม)" in page.title():
                isdisamtitle = True
            if "p107" in data["claims"]:
                for claim in data["claims"]["p107"]:
                    if claim.getTarget() == disamitem:
                        isdisam = True
                    if claim.getTarget() == wrongdisamitem:
                        wrongdisam = claim
            if wrongdisam:
                pywikibot.output("wrong disam item :(")
                claim.changeTarget(disamitem)
                isdisam = True
            elif (isdisamtitle) and (not isdisam):
                claim = pywikibot.Claim(datasite, "p107")
                claim.setTarget(disamitem)
                claim2 = pywikibot.Claim(datasite, "p143")
                claim2.setTarget(thwikiitem)
                item.addClaim(claim)
                claim.addSource(claim2)
                pywikibot.output("added claim!")
                isdisam = True
            oldlabels = None
            if "th" in data["labels"]:
                oldlabels = data["labels"]["th"]
            labels = lre.pats["rmdisam"].sub("", page.title())
            if not lre.pats["thai"].search(labels):
                continue
            if labels != oldlabels:
                pywikibot.output("old label: " + unicode(oldlabels))
                pywikibot.output("new label: " + unicode(labels))
                editdict["labels"] = labels
            if isdisam and (("th" in data["descriptions"] and
                            data["descriptions"]["th"] != descdisam) or
                            ("th" not in data["descriptions"])):
                editdict["descriptions"] = descdisam
            out = transform(editdict)
            if not out:
                continue
            pywikibot.output("item: " + qitem)
            pywikibot.output("title: " + page.title())
            try:
                item.editEntity(out)
            except:
                wp.error()
                pass

if __name__ == "__main__":
    sites = [pywikibot.getSite("wikidata", "wikidata")]
    args, site, conf = wp.pre("fill label", lock=True, sites=sites)
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        pass
        wp.post()
