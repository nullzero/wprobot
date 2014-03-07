#!/usr/bin/python
# -*- coding: utf-8 -*-

import init
import wp
import pywikibot
from wp import lre, ltime
from pywikibot.data import api
    
def glob():
    pass

def main():
    today = ltime.datetime.date.today()

    year = today.year + 543    
    month = libdate.monthThai(today.month)
    day = today.day

    for i in range(1, libdate.getNumDay(today.year, today.month) + 1):
        page = wp.Page(u"แม่แบบ:เหตุการณ์ปัจจุบัน/{} {} {}".format(year, month, i))
        if not page.exists():
            pywikibot.output(u"Create day %d" % i)
            page.put(
u"""{{เหตุการณ์ปัจจุบัน/วันเดือนปี|%d|%d|%d}}

<!-- ข่าวอยู่เหนือบรรทัดนี้ -->|}""" % (today.year, today.month, i)
                , u"เตรียมเหตุการณ์วันที่ %d %s %d ด้วยบอต" % (i, month, year))

    page = wp.Page(u"{} พ.ศ. {}".format(month, year))
    if not page.exists():
        content = u"""'''%s พ.ศ. %d''' เป็นเดือนที่ %d ของปี [[พ.ศ. %d]] \
วันแรกของเดือนเป็น[[%s]] วันสุดท้ายของเดือนเป็น[[%s]]

== [[สถานีย่อย:เหตุการณ์ปัจจุบัน]] ==
{{เหตุการณ์ปัจจุบัน/เดือน|%d %s}}

{{เหตุการณ์เดือนอื่น}}

[[หมวดหมู่:พ.ศ. %d แบ่งตามเดือน|*%d-%d]]

[[en:%s %d]]""" % (month, year, today.month, year, 
    libdate.weekdayThai(libdate.date(today.year, today.month, 1).weekday()),
    libdate.weekdayThai(libdate.date(today.year, today.month, 
        libdate.getNumDay(today.year, today.month)).weekday()),
    year, month,
    year, year, today.month,
    libdate.monthEng(today.month), today.year)
        page.put(content, u"เพิ่มเดือนโดยบอต")

args, site, conf = wp.pre(13, main=__name__)
try:
    glob()
    main()
except:
    wp.posterror()
else:
    wp.post()
    