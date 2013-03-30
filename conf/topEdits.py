# -*- coding: utf-8 -*-
"""
This is a user configuration file.
"""

import init
from wp import lre

path = u"วิกิพีเดีย:รายชื่อชาววิกิพีเดียที่แก้ไขมากที่สุด_500_อันดับ"
botsuffix = u"_(รวมบอต)"
maxnum = 5000
allentries = 500
summary = u"ปรับปรุงรายการ"
patbot = [u"(?i)^(?:บอต|bot)",
          u"(?i)(?:บอต|bot)$",
          u"(?i)^New user message$",
          u"(?i)^Redirect fixer$"]

for i, pat in enumerate(patbot):
    patbot[i] = lre.lre(pat)
