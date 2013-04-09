# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import sys
import init
from wp import lre

def matchbrace(s, i):
    lv = 0
    for i in xrange(i, len(s)):
        if s[i] == "{": lv += 1
        elif s[i] == "}": lv -= 1
        if lv == 0:
            return i

def main():
    s = """<div style="float:{{{float|left}}}; border:{{{border-width|{{{border-s|1}}}}}}px solid {{{border-color|{{{1|{{{border-c|{{{id-c|#999}}}}}}}}}}}}; margin:1px; width:238px;" class="wikipediauserbox {{{bodyclass|}}}">
{| style="border-collapse:collapse; width:238px; margin-bottom:0; background:{{{info-background|{{{2|{{{info-c|#EEE}}}}}}}}}"
{{#if:{{{logo|{{{3|{{{id<includeonly>|</includeonly>}}}}}}}}}|
! style="border:0; width:{{{logo-width|{{{id-w|45}}}}}}px; height:{{{logo-height|{{{id-h|45}}}}}}px; background:{{{logo-background|{{{1|{{{id-c|#DDD}}}}}}}}}; text-align:{{{id-a|center}}}; font-size:{{{logo-size|{{{5|{{{id-s|14}}}}}}}}}pt; color:{{{logo-color|{{{id-fc|black}}}}}}; padding:{{{logo-padding|{{{id-p|0 1px 0 0}}}}}}; line-height:{{{logo-line-height|{{{id-lh|1.25em}}}}}}; vertical-align: middle; {{{logo-other-param|{{{id-op|}}}}}}" {{#if:{{{id-class|}}}|class="{{{id-class}}}"}} {{!}} {{{logo|{{{3|{{{id|id}}}}}}}}}
}}
| style="border:0; text-align:{{{info-a|left}}}; font-size:{{{info-size|{{{info-s|8}}}}}}pt; padding:{{{info-padding|{{{info-p|0 4px 0 4px}}}}}}; height:{{{logo-height|{{{id-h|45}}}}}}px; line-height:{{{info-line-height|{{{info-lh|1.25em}}}}}}; color:{{{info-color|{{{info-fc|black}}}}}}; vertical-align: middle; {{{info-other-param|{{{info-op|}}}}}}" {{#if:{{{info-class|}}}|class="{{{info-class}}}"}} | {{{info|{{{4|''info''}}}}}}
|}</div>{{#if:{{{usercategory|}}}{{{usercategory2|}}}{{{usercategory3|}}}|{{category handler
 |nocat = {{{nocat|}}}
 |subpage = {{#if:{{{nocatsubpages|}}}|no}}
 |user = {{#if:{{{usercategory|}}}|[[Category:{{{usercategory}}}]]}}{{#if:{{{usercategory2|}}}|[[Category:{{{usercategory2}}}]]}}{{#if:{{{usercategory3|}}}|[[Category:{{{usercategory3}}}]]}}
 |template = {{#if:{{{usercategory|}}}|[[Category:{{{usercategory}}}| {{BASEPAGENAME}}]]}}{{#if:{{{usercategory2|}}}|[[Category:{{{usercategory2}}}| {{BASEPAGENAME}}]]}}{{#if:{{{usercategory3|}}}|[[Category:{{{usercategory3}}}| {{BASEPAGENAME}}]]}}
}}}}<noinclude>{{documentation}}</noinclude>"""
    lst = []
    for i in lre.finditer(r"\{\{\{\s*" + "usercategory" + "\s*[\|\}]", s):
        begin, end = i.span()
        end = matchbrace(s, begin)
        lst.append((begin, "begin"))
        lst.append((end, "end"))
    lst = sorted(lst)
    lst.append((sys.maxint, sys.maxint))
    ilst = 0
    out = []
    for i in xrange(len(s)):
        if i == lst[ilst][0]:
            if lst[ilst][1] == "begin":
                out.append("{{{หมวดหมู่|")
            else:
                out.append("}}}")
            ilst += 1
        out.append(s[i])
    print "".join(out)
"""
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
"""
main()
