# -*- coding: utf-8  -*-
"""Fill label!"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from wp import lre
from pywikibot.tools import itergroup

def glob():
    lre.pats["rmdisam"] = lre.lre(ur"\s+\([^\(]*?\)\s*$")
    lre.pats["thai"] = lre.lre(u"[\u0e00-\u0e7f]")

def transform(dic):
    out = {}
    for i in dic:
        out[i] = {"th": {"language": "th", "value": dic[i]}}
    return out

def main():
    datasite = site.data_repository()
    disamitem = pywikibot.ItemPage(datasite, "Q11651459")
    thwikiitem = pywikibot.ItemPage(datasite, "Q565074")
    wrongdisamitem = pywikibot.ItemPage(datasite, "Q4167410")
    descdisam = u"หน้าแก้ความกำกวมวิกิพีเดีย"
    for pages in itergroup(site.allpages(filterredir=False, start=u"ก"), 100):
        dat = datasite.loadcontent({"sites": site.dbName(),
                                    "titles": "|".join([page.title()
                                                        for page in pages])})

        for i, qitem in enumerate(dat):
            if not qitem.startswith("q"): continue
            pywikibot.output("item: " + qitem)
            item = pywikibot.ItemPage(datasite, qitem)
            item._content = dat[qitem]
            super(pywikibot.ItemPage, item).get() # For getting labels
            data = item.get()
            editdict = {}
            isdisam = False
            isdisamtitle = False
            wrongdisam = None
            page = wp.Page(item.getSitelink(site))
            pywikibot.output("title: " + page.title())
            #if page.title() in [u"ซันนี (Sunny)", u"ซันนี (Sonny)"]: continue
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
                pywikibot.output("old label: " + oldlabels)
                pywikibot.output("new label: " + labels)
                editdict["labels"] = labels
            if isdisam and (("th" in data["descriptions"] and
                            data["descriptions"]["th"] != descdisam) or
                            ("th" not in data["descriptions"])):
                editdict["descriptions"] = descdisam
            out = transform(editdict)
            if not out:
                pywikibot.output("skip! nothing to do")
                continue
            item.editEntity(out)

if __name__ == "__main__":
    args, site, conf = wp.pre("fill label")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        pass
        wp.post()
