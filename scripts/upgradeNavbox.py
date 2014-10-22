#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from wp import lre
from pywikibot.data import api

def glob():
    patintclass = lre.lre(ur"(?ms)\|\s*title\s*=(.*?)$")
    delimit = [ur"\s*[\•\·]\s*", ur"\ +[\•\.\·\-] +", ur"\ *\{\{(?:[\,\•·]|[\•\·\!]w|·wrap|จุด)\}\}\s*", ur"\s*\&\#124\;\s*"]
    delimit = lre.sep(delimit) + ur"(?!(?:(?![\[\]]).)*\])"
    patdel = lre.lre(u"(?s)(\|\ *list\d+(?:(?!below|seealso|" + #u"(?<=\]\])" + 
             delimit + u").)*)" + #u"(?<=\]\])" + 
            delimit)
    patnl = lre.lre(u"(list\d+)\s*=\s*(?![\|\s\}])")
    patwrap = lre.lre(u"\{\{[Nn]owrap\s*(?:\|(.*?))?\}\}\ *")
    patrmwrap = lre.lre(u"\{\{[Nn]owrap.*?\}\}\ *")
    triml = lre.lre(u"\n+")
    patbr = lre.lre(u"(?m)^(\*[^\n]*)<\s*/?\s*br\s*/?\s*>")
    alltag = [u"small", u"span", u"div"]
    patopen = lre.lre(u"(?m)^\*\ *(<" + lre.sep(alltag) + u">)\s*\[\[")
    patclose = lre.lre(u"\]\]\ *(</" + lre.sep(alltag) + u">)")

def process(page)

def main():
    if args:
        gen = [wp.Page(wp.handlearg("page", args))]
    else:
        gen = pywikibot.Category(site, u'กล่องนำทางที่ไม่ได้ใช้รายการแนวนอน').articles()
    namespass = libinfo.getdat(filename=u"passlist", key=u"name")
    namespass = filter(lambda x: x, 
            [x.strip() for x in (namespass if namespass else "").split(u" ")])
    for page in gen:
        print ">>>", page.title()
        if not page.title().startswith(u"แม่แบบ:"):
            continue
        
        if page.title().replace(u" ", u"_") in namespass:
            print "pass!"
            continue
        try:
            text = page.get()
        except:
            preload.error()
            continue
        
        addlistclass = True
        addhlist = True
        if u"listclass" in text:
            addlistclass = False
        
        if u"hlist" in text:
            addhlist = False
        
        print "listclass :", addlistclass, "hlist :", addhlist, 
        
        if addlistclass and addhlist:
            text = text.replace(u"กล่องท้ายเรื่องใหม่", u"navbox")
            text = patintclass.sub(u"| title = \\1\n| listclass = hlist", text)
            odiff = text
            text = patwrap.sub(u"\\1", text)
            text = patdel.subr(u"\\1\n* ", text)
            text = patnl.sub(u"\\1 = \n* ", text)
            text = triml.sub(u"\n", text)
            text = patbr.sub(u"\\1", text)
            text = patopen.sub(u"\\1\n* [[", text)
            text = patclose.sub(u"]]\n\\1", text)
            text = text.replace(u"&nbsp;", u"")
            text = patrmwrap.sub(u"", text)
            
            #text = patfix.sub(, text)
            print text
            print "------------"
            pywikibot.showDiff(odiff, text)
            print "------------"
            print ">>>", page.title()
            response = raw_input("Should proceed?: ")
            if response == 'y' or response == '':
                page.put(text, u"ปรับปรุงแม่แบบ Navbox")
            elif response == 'p':
                namespass.append(page.title().replace(u" ", u"_"))
                libinfo.putdat(filename=u"passlist", key=u"name", 
                                value=" ".join(namespass))

    

args, site, conf = wp.pre(12, main=__name__)
try:
    wp.run(main)
except:
    wp.posterror()
else:
    wp.post()
