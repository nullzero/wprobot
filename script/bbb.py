import pywikibot
import random

site = pywikibot.getSite()
page = pywikibot.Page(site, u"วิกิพีเดีย:ทดลองเขียน")
page.put(unicode(chr(random.randint(ord('A'), ord('Z') + 1))), u"ทดสอบการทำงาน2")
