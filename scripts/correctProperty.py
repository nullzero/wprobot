# -*- coding: utf-8 -*-

import init
import wp
import pywikibot

"""
Begin helper function
"""

def glob():
    pass

def main():
    global site
    site = site.data_repository()
    prop = pywikibot.Page(site, "Property:P140")
    #print prop
    #print prop.get()
    for page in prop.backlinks():
        try:
            if page.namespace() == 0 and page.title().startswith("Q"):
                page = pywikibot.ItemPage(site, page.title())
                content = page.get()
                print ">>>", page.title()
                for claim in content["claims"]["p140"]:
                    target = claim.getTarget()
                    links = target.get()["sitelinks"]
                    if "thwiki" in links:
                        print "thwiki", links["thwiki"]
                    else:
                        print "enwiki", links["enwiki"]
        except:
            wp.error()

if __name__ == "__main__":
    args, site, conf = wp.pre(u"update top things in Wikipedia")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
