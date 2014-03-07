#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Fix misspelled words
"""

import init
import wp
import pywikibot
from wp import lre

def glob():
    global subst
    subst = lre.Subst()
    subst.append(u"กฏหมาย", u"กฎหมาย")
    subst.append(u"กรกฏาคม", u"กรกฎาคม")
    subst.append(u"กษัตรย์", u"กษัตริย์")
    subst.append(u"กิติมศักดิ์", u"กิตติมศักดิ์")
    subst.append(u"ขาดดุลย์", u"ขาดดุล")
    subst.append(u"คริสตศตวรรษ", u"คริสต์ศตวรรษ")
    subst.append(u"คริสตศักราช", u"คริสต์ศักราช")
    subst.append(u"คริสตศาสนา", u"คริสต์ศาสนา")
    subst.append(u"คริสต์กาล", u"คริสตกาล")
    subst.append(u"คริสต์เตียน", u"คริสเตียน")
    subst.append(u"คริส(ต์)?มาส(ต์)?", u"คริสต์มาส")
    subst.append(u"โครงการณ์", u"โครงการ")
    subst.append(u"งบดุลย์", u"งบดุล")
    subst.append(u"ซอฟท์แวร์", u"ซอฟต์แวร์")
    subst.append(u"ฟัง[กค]์ชั่?น", u"ฟังก์ชัน")
    subst.append(u"ภาพยนต์", u"ภาพยนตร์")
    subst.append(u"ผูกพันธ์", u"ผูกพัน")
    subst.append(u"ลอส ?แองเจ[นลอ]?ล[ีิ]ส", u"ลอสแอนเจลิส")
    subst.append(u"ลายเซ็นต์", u"ลายเซ็น")
    subst.append(u"เวคเตอร์", u"เวกเตอร์")
    subst.append(u"เวท(ย์)?มนตร?์", u"เวทมนตร์")
    subst.append(u"เว็?[บป]ไซ[ทต]์?", u"เว็บไซต์")
    subst.append(u"เวอร์ชั่น", u"เวอร์ชัน")
    subst.append(u"อินเ[ตท]อ(ร์)?เน็?[ตท]", u"อินเทอร์เน็ต")
    subst.append(u"อั[พป]เด็?[ตท]", u"อัปเดต")
    subst.append(u"อัพโหลด", u"อัปโหลด")
    subst.append(u"(?m)^(=+) *(.*?) *(=+) *$", ur"\1 \2 \3")
    subst.append(u"(?m)^= (.*?) =$", ur"== \1 ==")
    subst.append(u"\[\[(:?)[Cc]ategory:", ur"[[\1หมวดหมู่:")
    subst.append(u"\[\[(:?)([Ii]mage|[Ff]ile|ภาพ):", ur"[[\1ไฟล์:")
    subst.append(u"(?m)^== (แหล่ง|หนังสือ|เอกสาร|แหล่งข้อมูล)อ้างอิง ==$", u"== อ้างอิง ==")
    subst.append(u"(?m)^== (หัวข้ออื่นที่เกี่ยวข้อง|ดูเพิ่มที่) ==$", u"== ดูเพิ่ม ==")
    subst.append(u"(?m)^== (เว็บไซต์|โยง|ลิงก์|Link *|(แหล่ง)?(ข้อมูล)?)(ภายนอก|อื่น) ==$", u"== แหล่งข้อมูลอื่น ==")
    subst.append(u"(?m)^== ลิงก์ ==$", u"== แหล่งข้อมูลอื่น ==")
    subst.append(u"\{\{[Rr]eflist", u"{{รายการอ้างอิง")
    subst.append(ur"\[\[ *(.*?)\]\]", ur"[[\1]]")
    subst.append(ur"\[\[(?!หมวดหมู่)(.*?) *\]\]", ur"[[\1]]")
    subst.append(u"(?<!วัด)ทรง(เสวย|ประชวร|มีพระ|เป็นพระ|เสด็จ|บรรทม|ผนวช|ทอดพระเนตร|สวรรคต|ตรัส|โปรด|ประสูติ)", r"\1")

def fix(s):
    if "nofixbot" in s:
        return s
    return subst.process(s)

def main():
    #tl = wp.Page(u"Template:บาเบล")
    for page in site.allpages(filterredir=False, content=True):
    #for page in tl.embeddedin(content=True):
    #for page in tl:
        #page = wp.Page(u"รายชื่อวัดในจังหวัดชัยนาท")
        pywikibot.output(">>>" + page.title())
        text = fix(page.get())
        if page.get() != text:
            pywikibot.showDiff(page.get(), text)
            if raw_input("...") == "y":
                try:
                    page.put(text, u"โรบอต: เก็บกวาด", async=True)
                except:
                    wp.error()
                    pass

if __name__ == "__main__":
    args, site, conf = wp.pre(u"user-fixes")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
