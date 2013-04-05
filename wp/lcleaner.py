# -*- coding: utf-8  -*-
"""
Clean! Clean! Clean!
"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
from wp import llang, lre

def consecutiveSpace(s):
    """Remove consecutive spaces."""
    s = s.group()
    prefix = ""
    if s.startswith("</source>"):
        prefix = "</source>"
        s = s[len("</source>"):]
    return prefix + patListSpace.process(s)

""" Section ========================================================="""

patListSection = lre.subst()
patListSection.append(("'{2,}", ""))
# remove all italic and bold markup
patListSection.append(("<(?!/?(ref|sup|sub)).*?>", ""))
# remove all html markup except refupub

""" Table ==========================================================="""

patListTable = lre.subst()
patListTable.append((r"(?m)^(\|[\-\+\}]?) *", r"\1 "))
# "$|-abc$" => "$|- abc$", "$|-$" => "$|- $"
patListTable.append((r" *\|\| *", " || "))
# "$z||a$" => "$z || a$"
patListTable.append((" *!! *", " !! "))
# "$z!!a$" => "$z !! a$"
patListTable.append((r"(?m)^\|([\}\-$]) *$", r"|\1"))
# "$|- $" => "$|-$"
patListTable.append(("(?m)^! *", "! "))
# "$!abc !! asd$" => "$! abc !! asd$"

""" Space ==========================================================="""
patListSpace = lre.subst()
patListSpace.append(("(?m)(?<=^)(?! )(.*?) +", r"\1 "))
# "$abc    def   ghi$" => "$abc def ghi$"
# except: that line is in source tag or that line starts with space

patList = lre.subst()
patList.append((r"[\t\r\f\v]", " "))
# change all whitespaces to space!
patList.append((r"_(?=[^\[\]]*\]\])", " "))
# $[[_abc_def_]]$ => $[[ abc def ]]$
patList.append((r"(?m)(?<!=) +$", ""))
# strip traling space
patList.append((r"(?m)=$", "= "))
# strip traling space except the last character is =
patList.append((r"(?m)^(=+) *(.*?) *(=+) *$", r"\1 \2 \3"))
# $==   oak   ==   $ => $== oak ==$
patList.append((r"(?m)^= (.*?) =$", r"== \1 =="))
# don't use first-level headings
patList.append((r"(?m)^==+\ .*?\ ==+$", patListSection.process))
# call patListSection
tablemarkup = ["rowspan", "align", "colspan", "width", "style"]
patList.append(("(" + lre.sep(tablemarkup) + ") *= *", r"\1 = "))
# clean whitespace around equal sign
patList.append((r"\[\[ *(.*?) *\]\]", r"[[\1]]"))
# $[[   abc   def   ]]$ => $[[abc   def]]$
patList.append((r"\[\[(:?)[Cc]ategory:", ur"[[\1หมวดหมู่:"))
# L10n
patList.append((ur"\[\[(:?)([Ii]mage|[Ff]ile|ภาพ):", ur"[[\1ไฟล์:"))
# L10n
patList.append((u"(?m)^== (แหล่ง|หนังสือ|เอกสาร|แหล่งข้อมูล)อ้างอิง ==$",
                u"== อ้างอิง =="))
# อ้างอิง
patList.append((u"(?m)^== (หัวข้ออื่นที่เกี่ยวข้อง|ดูเพิ่มที่) ==$",
                u"== ดูเพิ่ม =="))
# ดูเพิ่ม
patList.append((ur"""(?mx)^==\ (เว็บไซต์|โยง|ลิง[กค]์|Link *|(แหล่ง)?ข้อมูล)
                (ภายนอก|อื่น)\ ==$""", u"== แหล่งข้อมูลอื่น =="))
# แหล่งข้อมูลอื่น
patList.append((r"(?m)^(:*)([#\*]+) *", r"\1\2 "))
# clean whitespace after indentation and bullet
patList.append((r"(?m)^(:+)(?![\*#]) *", r"\1 "))
# clean whitespace after indentation and bullet
patList.append((r"(?m)^(:*)([\*#]*) \{\|", r"\1\2{|"))
# but openning tag of table must stick with front symbol
# "$:::** {|$" => "$:::**{|$"
patList.append((r"(?m)^\|(?![\}\+\-]) *", "| "))
# clean whitespace for template and table, except |+ |- |}
# "$|asdasd$" => "$| asdasd$"
patList.append(("(?ms)^\{\|.*^\|\}.*?$", patListTable.process))
# call patListTable
patList.append(("<references */ *>(?!.*<references */ *>)",
                u"{{รายการอ้างอิง}}"))
# L10n / if there are more than one reference tags, don't change!
patList.append(("(?i)\{\{ *Reflist *", u"{{รายการอ้างอิง"))
# L10n
patList.append((r"(?ms)((?:</source>)?)(?:(?!</?source>).)*(?=<source>|\Z)",
                consecutiveSpace))
# call consecutiveSpace!

def clean(s):
    """Clean text!"""
    return patList.process(llang.fixRepetedVowel(s))
