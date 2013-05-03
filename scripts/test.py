# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from wp import lre

def glob():
    pass

a = u"""asd
asd

==French==

===Pronunciation===
* {{homophones|accaparent|accapares}}

===Verb===
{{fr-verb-form}}

# {{conjugation of|accaparer||1|s|pres|ind|lang=fr}}
# {{conjugation of|accaparer||3|s|pres|ind|lang=fr}}
# {{conjugation of|accaparer||1|s|pres|sub|lang=fr}}
# {{conjugation of|accaparer||1|s|pres|sub|lang=fr}}
# {{conjugation of|accaparer||2|s|imp|lang=fr}}

==Germany==

===Pronunciation===
* {{homophones|accaparent|accapares}}

[[fr:accapare]]
[[li:accapare]]
[[mg:accapare]]"""

def homophix(match):
    print match.group()
    print "-" * 100
    return lre.sub(r'(\{\{homophones\|)([^}=]*\}\})',
                  r'\1lang={{subst:langrev|'+match.group(1)+r'}}|\2',
                  match.group(0)
                  )

def main():
    page = wp.Page("wikt:en:accapare")
    text = page.get()
    text = a
    print text
    print "-" * 100
    #print lre.sub(ur'(?m)^==([a-zA-Z ]+) *==\n+(?:(?:===|[^=]).*\n+)*', homophix, text)
    print lre.search(r'(?ms)^== *([^\n]+) *== *((?!==(?!=))[^\n]*\n)*', text).group()

if __name__ == "__main__":
    args, site, conf = wp.pre("test")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        pass
        wp.post()
