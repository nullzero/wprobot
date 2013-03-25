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
    prefix = u""
    if s.startswith(u"</source>"):
        prefix = u"</source>"
        s = s[len(u"</source>"):]
    return prefix + patListSpace.do(s)

""" Section ========================================================="""

patListSection = lre.subst()
patListSection.append((u"'''", u""))
# remove all bold markup
patListSection.append((u"''", u""))
# remove all italic markup
patListSection.append((u"<(?!/?(ref|sup|sub)).*?>", u""))
# remove all html markup except refupub

""" Table ==========================================================="""

patListTable = lre.subst()
patListTable.append((ur"(?m)^(\|[\-\+\}]?) *", ur"\1 "))
# "$|-abc$" => "$|- abc$", "$|-$" => "$|- $"
patListTable.append((ur" *\|\| *", u" || "))
# "$z||a$" => "$z || a$"
patListTable.append((u" *!! *", u" !! "))
# "$z!!a$" => "$z !! a$"
patListTable.append((ur"(?m)^\|([\}\-$]) *$", ur"|\1"))
# "$|- $" => "$|-$"
patListTable.append((u"(?m)^! *", u"! "))
# "$!abc !! asd$" => "$! abc !! asd$"

""" Space ==========================================================="""
patListSpace = lre.subst()
patListSpace.append((u"(?m)(?<=^)(?! )(.*?) +", ur"\1 "))
# "$abc    def   ghi$" => "$abc def ghi$"
# except: that line is in source tag or that line starts with space

patList = lre.subst()
patList.append((ur"[\t\r\f\v]", u" "))
# change all whitespaces to space!
patList.append((ur"_(?=[^\[\]]*\]\])", u" "))
# $[[_abc_def_]]$ => $[[ abc def ]]$
patList.append((ur"(?m)(?<!=) +$", u""))
# strip traling space
patList.append((ur"(?m)=$", u"= "))
# strip traling space except the last character is =
patList.append((ur"(?m)^(=+) *(.*?) *(=+) *$", ur"\1 \2 \3"))
# $==   oak   ==   $ => $== oak ==$
patList.append((ur"(?m)^= (.*?) =$", ur"== \1 =="))
# don't use first-level headings
patList.append((ur"(?m)^==+\ .*?\ ==+$", patListSection.do))
# call patListSection
tablemarkup = [u"rowspan", u"align", u"colspan", u"width", u"style"]
patList.append((u"(" + lre.sep(tablemarkup) + u") *= *", ur"\1 = "))
# clean whitespace around equal sign
patList.append((ur"\[\[ *(.*?) *\]\]", ur"[[\1]]"))
# $[[   abc   def   ]]$ => $[[abc   def]]$
patList.append((ur"\[\[(:?)[Cc]ategory:", ur"[[\1หมวดหมู่:"))
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
patList.append((ur"(?m)^(:*)([#\*]+) *", ur"\1\2 "))
# clean whitespace after indentation and bullet
patList.append((ur"(?m)^(:+)(?![\*#]) *", ur"\1 "))
# clean whitespace after indentation and bullet
patList.append((ur"(?m)^(:*)([\*#]*) \{\|", ur"\1\2{|"))
# but openning tag of table must stick with front symbol
# "$:::** {|$" => "$:::**{|$"
patList.append((ur"(?m)^\|(?![\}\+\-]) *", u"| "))
# clean whitespace for template and table, except |+ |- |}
# "$|asdasd$" => "$| asdasd$"
patList.append((u"(?ms)^\{\|.*^\|\}.*?$", patListTable.do))
# call patListTable
patList.append((u"<references */ *>(?!.*<references */ *>)",
                u"{{รายการอ้างอิง}}"))
# L10n / if there are more than one reference tags, don't change!
patList.append((u"(?i)\{\{ *Reflist *", u"{{รายการอ้างอิง"))
# L10n
patList.append((ur"(?ms)((?:</source>)?)(?:(?!</?source>).)*(?=<source>|\Z)",
                consecutiveSpace))
# call consecutiveSpace!

def clean(s):
    """Clean text!"""
    return patList.do(llang.fixRepetedVowel(s))
