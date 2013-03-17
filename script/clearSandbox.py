# -*- coding: utf-8  -*-
import pywikibot
import random

site = pywikibot.getSite()
page = pywikibot.Page(site, u"วิกิพีเดีย:ทดลองเขียน")
page.put(unicode(random.randint(1, 100000)), u"ทดสอบการทำงาน")
pywikibot.output(unicode(__file__))

import bbb

pywikibot.stopme()
