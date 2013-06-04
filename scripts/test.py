#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot

def glob():
    pass

def main():
    allpages = """Invert
Ipb-blocklist
Ipb-unblock-addr
Ipbexpiry
Ipbother
Ipbreason
Isredirect
Istemplate
Jumptosearch
Last
Linksearch-line
Linksearch-ok
Livepreview-loading
Lockbtn
Lockdb
login
loginerror
loginreqlink
loginsuccesstitle
logout
mimesearch
minoreditletter
move
movethispage
mycontris
mywatchlist
namespacesall
navigation
ncategories
nchanges
newarticle
newpageletter
newpages
newsectionsummary
next
nextn
nlinks
noemailtitle
nstab-category
nstab-image
nstab-mediawiki
nstab-template
nstab-user
ok
page_first
page_last
pagecategories
pagesize
pagetitle
permalink
personaltools
powersearch-field
prefs-edits
prefs-email
prefs-misc
prefs-watchlist
preview
prevn
print
protect
protectedarticle
protectedpages
protectthispage
proxyblocksuccess
randomredirect
rclinks
rcshowhidebots
rcshowhideliu
rcshowhidemine
rcshowhideminor
reblock-logentry"""
    allpages = allpages.split("\n")
    for page in allpages:
        if not page: continue
        page = wp.Page("MediaWiki:" + page)
        pageo = page.toggleTalkPage()
        if page.exists():
            page.delete(reason="= translatewiki", prompt=False)
        if pageo.exists():
            print ">>>", pageo.title()

    """
    for page in site.allpages(prefix=u"พระจักรพรรดิ", filterredir=True):
        pageReal = page.getRedirectTarget()
        for bPage in page.backlinks(content=True):
            bPage.put(bPage.get().replace(page.title(), pageReal.title()),
                      u"โรบอต: แก้ไขคำผิด (แจ้งโดยคุณเอ็ดมัน)", async=True)
        if len(list(page.backlinks())) > 0: continue
        page.delete(reason=u"ชื่อผิด (แจ้งโดยคุณเอ็ดมัน)", prompt=False)
    """

if __name__ == "__main__":
    args, site, conf = wp.pre(0)
    try:
        glob()
        wp.run(main)
    except:
        wp.posterror()
    else:
        wp.post()
