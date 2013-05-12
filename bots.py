# -*- coding: utf-8 -*-
"""Control panel"""

__version__ = "1.0.0"
__author__ = "Sorawee Porncharoenwase"

import wprobot
import wp
import pywikibot
from wp import ltime, lrepeat, lwikitable
import ctrl

def glob():
    pass

def check(revision):
    page = wp.Page(revision["title"])
    if page.title(withNamespace=False) != u"Nullzerobot/แผงควบคุม":
        return
    txt = page.get()
    try:
        header, table = lwikitable.wiki2table(txt)

    except:
        wp.error()

def main():
    for rev in lrepeat.repeat(site, site.recentchanges, lambda x: x["revid"],
                              60, showRedirects=False, showBot=False,
                              changetype=["edit"], namespaces=2,
                              start=site.getcurrenttime() - ltime.td(days=1)):
        try:
            check(rev)
        except:
            wp.error()

if __name__ == "__main__":
    args, site, conf = wp.pre("Nullzerobot control panel!")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
