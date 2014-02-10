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
    """
    site.login(True)
    site.logout()
    site.login(False)
    """
    site.login(False)
    print site.user()
    print api.Request(site=pywikibot.getSite("th"), action='query', meta='allmessages|siteinfo', ammessages="abusefilter-accountreserved|january").submit()
    #today = ltime.datetime.date.today()
    #print site.months_names
    
    #print site.mediawiki_messages("*")

#     year = today.year + 543    
#     month = libdate.monthThai(today.month)
#     day = today.day
# 
#     for i in range(1, libdate.getNumDay(today.year, today.month) + 1):
#         pageName = u"แม่แบบ:เหตุการณ์ปัจจุบัน/%d_%s_%d" % (year, month, i)
#         if not miscellaneous.existPage(pageName):
#             pywikibot.output(u"Create day %d" % i)
#             page = pywikibot.Page(site, pageName)
#             page.put(
# u"""{{เหตุการณ์ปัจจุบัน/วันเดือนปี|%d|%d|%d}}
# 
# <!-- ข่าวอยู่เหนือบรรทัดนี้ -->|}""" % (today.year, today.month, i)
#                 , u"เตรียมเหตุการณ์วันที่ %d %s %d ด้วยบอต" % (i, month, year))
# 
#     pageName = u"%s_พ.ศ._%d" % (month, year)
#     if not miscellaneous.existPage(pageName):
#         page = pywikibot.Page(site, pageName)
#         content = u"""'''%s พ.ศ. %d''' เป็นเดือนที่ %d ของปี [[พ.ศ. %d]] \
# วันแรกของเดือนเป็น[[%s]] วันสุดท้ายของเดือนเป็น[[%s]]
# 
# == [[สถานีย่อย:เหตุการณ์ปัจจุบัน]] ==
# {{เหตุการณ์ปัจจุบัน/เดือน|%d %s}}
# 
# {{เหตุการณ์เดือนอื่น}}
# 
# [[หมวดหมู่:พ.ศ. %d แบ่งตามเดือน|*%d-%d]]
# 
# [[en:%s %d]]""" % (month, year, today.month, year, 
#     libdate.weekdayThai(libdate.date(today.year, today.month, 1).weekday()),
#     libdate.weekdayThai(libdate.date(today.year, today.month, 
#         libdate.getNumDay(today.year, today.month)).weekday()),
#     year, month,
#     year, year, today.month,
#     libdate.monthEng(today.month), today.year)
#         page.put(content, u"เพิ่มเดือนโดยบอต")
#         pywikibot.output(u"Write new month")
#     else:
#         pywikibot.output(u"Nothing to do!")    

if __name__ == "__main__":
    args, site, conf = wp.pre(13)
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
        