# -*- coding: utf-8  -*-
"""
Library to manage everything about date and time.
"""

__version__ = "1.0.2"
__author__ = "Sorawee Porncharoenwase"

import datetime
import time

def wrapMonth(m):
    """Convert zero-based month number to zero-based month number."""
    m -= 1
    if m < 0:
        m += 12
    if m >= 12:
        m -= 12
    return m

def weekdayThai(d):
    """Return Thai name of days of the week."""
    return map(lambda x: u"วัน" + x, 
                [u"จันทร์", u"อังคาร", u"พุธ", u"พฤหัสบดี", u"ศุกร์",
                u"เสาร์", u"อาทิตย์"])[d]

def monthEng(m):
    """Return English name of month."""
    return [u"January", u"February", u"March", u"April", u"May", u"June", 
            u"July", u"August", u"September", u"October", u"November",
            u"December"][wrapMonth(m)]

def monthThai(m):
    """Return Thai name of month."""
    return [u"มกราคม", u"กุมภาพันธ์", u"มีนาคม", u"เมษายน", u"พฤษภาคม",
            u"มิถุนายน", u"กรกฎาคม", u"สิงหาคม", u"กันยายน", u"ตุลาคม",
            u"พฤศจิกายน", u"ธันวาคม"][wrapMonth(m)]
            
def monthThaiAbbr(m):
    """Return Thai abbreviated name of month."""
    return [u"ม.ค.", u"ก.พ.", u"มี.ค.", u"เม.ย.", u"พ.ค.", u"มิ.ย.", 
            u"ก.ค.", u"ส.ค.", u"ก.ย.", u"ต.ค.", u"พ.ย.", u"ธ.ค."][wrapMonth(m)]

def getNumDay(year, month):
    """Return length of day in given month"""
    if month == 2:
        if year % 400 == 0:
            return 29
        elif year % 100 == 0:
            return 28
        elif year % 4 == 0:
            return 29
        else:
            return 28
        
    return [0, 31, 0, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month]

class dt(datetime.datetime):
    """Date class"""
