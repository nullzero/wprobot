import pywikibot
import random

site = pywikibot.getSite()
page = pywikibot.Page(site, u"วิกิพีเดีย:ทดลองเขียน")
page.put(unicode(randint(1, 100000)), u"ทดสอบการทำงาน")

import bbb
