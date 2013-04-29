#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Remove "Recent death" template from the page which have been inserted
this tag for long time.
"""

import init
import wp
import pywikibot
from wp import lre, ltime

def glob():
    global datenow, template
    template = wp.Page(conf.templateName)
    lre.pats["tl"] = lre.lre(ur"(?i)\{\{\s*%s\s*\}\}\s*" %
                     lre.sep([page.title(withNamespace=False) for page in
                             list(template.backlinks(filterRedirects=True)) +
                             [template]]))
    datenow = site.getcurrenttime()

def check(ts):
    distance = (datenow - ts).days
    pywikibot.output("distance = %d days" % distance)
    return distance >= conf.daylimit

def main():
    for page in template.embeddedin():
        pywikibot.output(u">>> %s" % page.title())
        history = page.fullVersionHistory()
        oldversion = history[0][3]
        erase, found = False, False
        for cntversion, version in enumerate(history):
            if cntversion == 0:
                 continue
            newversion = oldversion
            oldversion = version[3]
            if (lre.pats["tl"].search(newversion) and
                    (not lre.pats["tl"].search(oldversion))):
                erase = check(history[cntversion - 1][1])
                found = True
                break

        if not found:
            erase = check(history[-1][1])

        if erase:
            page.put(lre.pats["tl"].sub(u"", page.get()), conf.summary)

if __name__ == "__main__":
    args, site, conf = wp.pre(u"remove recent death template", lock=True)
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
