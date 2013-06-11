#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Test page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import wp
import pywikibot
from os import listdir
from os.path import isfile, join
import re

def getinfo(p, txt):
    obj = p.search(txt)
    if obj: return obj.group(1).strip()
    return ""

def massert(value, msg):
    if not value:
        print "error: " + msg
    return not  value

def main():
    mypath = "/home/sorawee/gis"

    onlyfiles = sorted([f for f in listdir(mypath) if f.startswith("display_data.aspx?id=") and
                                               isfile(join(mypath,f))])

    pPRO = re.compile('<span id="lb_PROV_NAM_T">(.*?)</span>')
    pID = re.compile('<span id="lb_POS_NO">(.*?)</span>')
    pNAME = re.compile('<span id="lb_POS_NAME_T">(.*?)</span>')
    pNAME2 = re.compile('<span id="lb_POS_NAME_G">(.*?)</span>')
    pADD = re.compile('<span id="lb_POS_ADD">(.*?)</span>')
    pMOO = re.compile('<span id="lb_POS_MOO">(.*?)</span>')
    pBAN = re.compile('<span id="lb_POS_BAN">(.*?)</span>')
    pROAD = re.compile('<span id="lb_POS_ROAD">(.*?)</span>')
    pTAM = re.compile('<span id="lb_TAM_NAME">(.*?)</span>')
    pAMP = re.compile('<span id="lb_AMP_NAM_T">(.*?)</span>')
    pSEA = re.compile('<span id="lb_POS_TERRITORIAL_SEA">(.*?)</span>')
    pLAT = re.compile('<span id="lb_POS_LAT">(.*?)</span>')
    pLONG = re.compile('<span id="lb_POS_LONG">(.*?)</span>')
    pROYAL1 = re.compile(u'<td><span class="style17">เล่มที่</span></td>\s*<td width="18%" class="style2">&nbsp;(\d*)</td>')
    pROYAL2 = re.compile(u'<td width="4%"><span class="style17">ตอนที่</span></td>\s*<td width="16%" class="style2">&nbsp;(\d*)</td>')
    pROYAL3 = re.compile(u'วันที่ประกาศ</span></td>\s*<td width="33%" class="style2">&nbsp;(.*?)</td>')
    line = {}
    for fname in onlyfiles:
        print ">>>", fname
        with open(join(mypath, fname), "r") as f:
            txt = f.read().decode("utf-8")
        ppro = getinfo(pPRO, txt)
        if massert(ppro, "pro"): continue
        pid = getinfo(pID, txt)
        if massert(pid, "id"): continue
        psea = getinfo(pSEA, txt)
        if massert(not psea, "sea"): continue
        pname = getinfo(pNAME, txt)
        if massert(pname, "name"): continue

        with open(join(mypath, fname.replace("display_data.aspx", "display_data4.aspx")), "r") as f:
            txt2 = f.read().decode("utf-8")
        proyal1 = getinfo(pROYAL1, txt2)
        proyal2 = getinfo(pROYAL2, txt2)
        proyal3 = getinfo(pROYAL3, txt2)
        massert(proyal1, "proyal1")
        massert(proyal2, "proyal2")
        massert(proyal3, "proyal3")
        #raw_input("...")
        if ppro not in line:
            line[ppro] = []
        line[ppro].extend([u"{{แถวโบราณสถาน",
                           u"| ทะเบียน = " + pid,
                           u"| ชื่อ = [[" + pname + "]]",
                           u"| ที่ตั้ง =" + ((u" เลขที่ %s" % getinfo(pADD, txt)) if getinfo(pADD, txt) else "") +
                                        ((u" หมู่ %s" % getinfo(pMOO, txt)) if getinfo(pMOO, txt) else "") +
                                        ((u" ถนน %s" % getinfo(pROAD, txt)) if getinfo(pROAD, txt) else ""),
                           u"| ตำบล = " + getinfo(pTAM, txt),
                           u"| อำเภอ = " + getinfo(pAMP, txt),
                           u"| lat = " + getinfo(pLAT, txt),
                           u"| lon = " + getinfo(pLONG, txt),
                           u"| ภาพ = ",
                           u"| ประกาศ = " + proyal3,
                           u"| อ้างอิง =" + ((u" เล่มที่ %s" % proyal1) if proyal1 else "") +
                                          ((u" ตอนที่ %s" % proyal2) if proyal2 else ""),
                           u"| ลิงก์ = " + "[http://www.gis.finearts.go.th/fad50/fad/" + fname + u" กรมศิลปากร]",
                           u"}}"
                     ])
        print "done"

    for province in line:
        if province == u"กรุงเทพมหานคร": continue
        print ">>>", province
        wp.Page(u"รายชื่อโบราณสถานในจังหวัด" + province + u"ที่ขึ้นทะเบียนโดยกรมศิลปากร").put(
u"""'''รายชื่อโบราณสถานในจังหวัด%(province)sที่ขึ้นทะเบียนโดยกรมศิลปากร'''

ต่อไปนี้เป็นรายชื่อโบราณสถานใน[[จังหวัด%(province)s]] ที่ขึ้นทะเบียนโดย[[กรมศิลปากร]]และประกาศใน[[ราชกิจจานุเบกษา]]แล้ว มีผลตาม[[:s:th:พระราชบัญญัติโบราณสถาน โบราณวัตถุ ศิลปวัตถุ และพิพิธภัณฑสถานแห่งชาติ พ.ศ. ๒๕๐๔/๒๕๓๕.๐๓.๒๙|พระราชบัญญัติโบราณสถาน โบราณวัตถุ ศิลปวัตถุ และพิพิธภัณฑสถานแห่งชาติ พ.ศ. ๒๕๐๔]]

{{หัวโบราณสถาน}}
%(body)s
|}

== แหล่งข้อมูลอื่น ==
<!--ใส่เว็บของจังหวัดถ้าจังหวัดนั้นได้รวบรวมข้อมูลแหล่งโบราณสถานไว้  สำหรับเว็บส่วนกลางอย่างกรมศิลป์ ราชกิจจานุเบกษา ไม่ต้องใส่แล้ว-->

{{โบราณสถานกรมศิลป์}}

[[หมวดหมู่:รายชื่อโบราณสถานที่ขึ้นทะเบียนโดยกรมศิลปากร|%(province)s]]
[[หมวดหมู่:โบราณสถานในจังหวัด%(province)s]]
[[หมวดหมู่:จังหวัด%(province)s]]""" % {"province": province, "body": "\n".join(line[province])}, u"เพิ่มเนื้อหาโดยบอต", async=True)

if __name__ == "__main__":
    args, site, conf = wp.pre(0)
    try:
        main()
    except:
        wp.posterror()
    else:
        wp.post()
