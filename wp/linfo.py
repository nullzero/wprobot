# -*- coding: utf-8  -*-
"""
Library to manage everything related to stroing information.
I/O can be file or wiki page.
"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"


import init
import wp
from wp import lre

def getdat(page, key=None):
    """
    Return value of given key, but if key is not given, return dict instead.
    """
    key = wp.toutf(key) if key else None
    text = page.get()
    if key:
        try:
            dat = lre.find(u"(?m)^\* " + lre.escape(key) + 
                           u": (.*?)$", text, 1)
            if dat:
                dat = wp.toutf(dat)
    else:
        lines = text.strip().split("\n")
        dat = {}
        for line in lines:
            key, value = line.split(": ")
            dat[key] = value
            
    return dat

def putdat(page, key, value):
    """
    Save value of given key.
    """
    key = wp.toutf(key)
    value = wp.toutf(value)
    text = page.get().strip()
    escapekey = lre.escape(key)
    text, changes = lre.subn(u"(?m)^\* %s: (.*?)$" % escapekey,
                             u"* %s: %s" % (escapekey, value),
                             text)
    # if there is no change, it means that we have to append new config.
    # However, don't check that newtext is equal to oldtext because
    # if newvalue is equal oldvalue, it will duplicate that key.
    if changes == 0:
        addedLine = u"* " + key + u": " + value
        if text:
            text = text + u"\n" + addedLine
        else:
            text = addedLine
    
    page.put(text, u"ปรับปรุงข้อมูล")
