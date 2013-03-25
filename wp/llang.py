# -*- coding: utf-8  -*-
"""
Library to manage everything about language (especially Thai language)
"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import pywikibot
from wp import lre

ThaiBegin = u"\u0e01"
ThaiEnd = u"\u0e5b"

Thai = {
    "Alphabet" : u"[%s-%s]" % (eval(repr(u"ก")), eval(repr(u"ฮ"))),
    "VowelFront" : u"เแโใไ",
    "VowelBack" : u"ะาๅ",
    "VowelUm" : u"ำ",
    "VowelUp" : u"ัิีึืํ",
    "VowelDown" : u"ฺุู",
    "VowelTaiku" : u"็",
    "Sound" : u"่้๊๋",
    "Tantakad" : u"์",
    "Paiyan" : u"ฯ",
    "Yamok" : u"ๆ",
}

Thai["All"] = u"".join([Thai[i] for i in Thai])
Thai["Not"] = u"^%s" % Thai["All"]

ASCII = {
    "Symbol" : u"".join([unichr(i) for i in xrange(128) if \
                        lre.search(u"[A-Za-z]", unichr(i))]),
}

def analyzeChar(content):
    """
    Return number of Thai characters and number of foreign characters.
    """
    cntThaiChar = 0
    cntForeignChar = 0
    
    for i in content:
        if i in Thai["All"]:
            cntThaiChar += 1
        else:
            cntForeignChar += 1
    
    return cntThaiChar, cntForeignChar

def cntWrongVowelHelper(x, y, line):
    """
    Helper function to count number of occurrences of impossible vowel
    arrangement.
    """
    cnt += lre.findOverlap(u"[" + x + u"]" + u"[" + y + u"]", line)

def cntWrongVowel(line):
    """Return number of occurrences of impossible vowel arrangement."""
    cnt = 0
    cnt += cntWringVowelHelper(Thai["VowelFront"], Thai["VowelFront"], line)
    cnt += cntWringVowelHelper(Thai["VowelFront"], Thai["VowelBack"], line)
    cnt += cntWringVowelHelper(Thai["VowelFront"], Thai["VowelUm"], line)
    cnt += cntWringVowelHelper(Thai["VowelFront"], Thai["VowelUp"], line)
    cnt += cntWringVowelHelper(Thai["VowelFront"], Thai["VowelDown"], line)
    cnt += cntWringVowelHelper(Thai["VowelFront"], Thai["VowelTaiku"], line)
    cnt += cntWringVowelHelper(Thai["VowelFront"], Thai["Sound"], line)
    cnt += cntWringVowelHelper(Thai["VowelFront"], Thai["Tantakad"], line)
    cnt += cntWringVowelHelper(Thai["VowelFront"], Thai["Paiyan"], line)
    cnt += cntWringVowelHelper(Thai["VowelFront"], Thai["Yamok"], line)
    cnt += cntWringVowelHelper(Thai["VowelFront"], Thai["Not"], line)
               
    cnt += cntWringVowelHelper(Thai["VowelBack"], Thai["VowelUm"], line)
    cnt += cntWringVowelHelper(Thai["VowelBack"], Thai["VowelUp"], line)
    cnt += cntWringVowelHelper(Thai["VowelBack"], Thai["VowelDown"], line)
    cnt += cntWringVowelHelper(Thai["VowelBack"], Thai["VowelTaiku"], line)
    cnt += cntWringVowelHelper(Thai["VowelBack"], Thai["Sound"], line)
    cnt += cntWringVowelHelper(Thai["VowelBack"], Thai["Tantakad"], line)
               
    cnt += cntWringVowelHelper(Thai["VowelUm"], Thai["VowelBack"], line)
    cnt += cntWringVowelHelper(Thai["VowelUm"], Thai["VowelUm"], line)
    cnt += cntWringVowelHelper(Thai["VowelUm"], Thai["VowelUp"], line)
    cnt += cntWringVowelHelper(Thai["VowelUm"], Thai["VowelDown"], line)
    cnt += cntWringVowelHelper(Thai["VowelUm"], Thai["VowelTaiku"], line)
    cnt += cntWringVowelHelper(Thai["VowelUm"], Thai["Sound"], line)
    cnt += cntWringVowelHelper(Thai["VowelUm"], Thai["Tantakad"], line)
               
    cnt += cntWringVowelHelper(Thai["VowelUp"], Thai["VowelBack"], line)
    cnt += cntWringVowelHelper(Thai["VowelUp"], Thai["VowelUm"], line)
    cnt += cntWringVowelHelper(Thai["VowelUp"], Thai["VowelUp"], line)
    cnt += cntWringVowelHelper(Thai["VowelUp"], Thai["VowelDown"], line)
    cnt += cntWringVowelHelper(Thai["VowelUp"], Thai["VowelTaiku"], line)
               
    cnt += cntWringVowelHelper(Thai["VowelDown"], Thai["VowelBack"], line)
    cnt += cntWringVowelHelper(Thai["VowelDown"], Thai["VowelUm"], line)
    cnt += cntWringVowelHelper(Thai["VowelDown"], Thai["VowelUp"], line)
    cnt += cntWringVowelHelper(Thai["VowelDown"], Thai["VowelDown"], line)
    cnt += cntWringVowelHelper(Thai["VowelDown"], Thai["VowelTaiku"], line)
               
    cnt += cntWringVowelHelper(Thai["VowelTaiku"], Thai["VowelBack"], line)
    cnt += cntWringVowelHelper(Thai["VowelTaiku"], Thai["VowelUm"], line)
    cnt += cntWringVowelHelper(Thai["VowelTaiku"], Thai["VowelUp"], line)
    cnt += cntWringVowelHelper(Thai["VowelTaiku"], Thai["VowelDown"], line)
    cnt += cntWringVowelHelper(Thai["VowelTaiku"], Thai["VowelTaiku"], line)
    cnt += cntWringVowelHelper(Thai["VowelTaiku"], Thai["Tantakad"], line)
               
    cnt += cntWringVowelHelper(Thai["Sound"], Thai["VowelUp"], line)
    cnt += cntWringVowelHelper(Thai["Sound"], Thai["VowelDown"], line)
    cnt += cntWringVowelHelper(Thai["Sound"], Thai["VowelTaiku"], line)
    cnt += cntWringVowelHelper(Thai["Sound"], Thai["Sound"], line)
    cnt += cntWringVowelHelper(Thai["Sound"], Thai["Tantakad"], line)
               
    cnt += cntWringVowelHelper(Thai["Tantakad"], Thai["VowelBack"], line)
    cnt += cntWringVowelHelper(Thai["Tantakad"], Thai["VowelUm"], line)
    cnt += cntWringVowelHelper(Thai["Tantakad"], Thai["VowelUp"], line)
    cnt += cntWringVowelHelper(Thai["Tantakad"], Thai["VowelDown"], line)
    cnt += cntWringVowelHelper(Thai["Tantakad"], Thai["VowelTaiku"], line)
    cnt += cntWringVowelHelper(Thai["Tantakad"], Thai["Sound"], line)
    cnt += cntWringVowelHelper(Thai["Tantakad"], Thai["Tantakad"], line)
               
    cnt += cntWringVowelHelper(Thai["Paiyan"], Thai["VowelBack"], line)
    cnt += cntWringVowelHelper(Thai["Paiyan"], Thai["VowelUm"], line)
    cnt += cntWringVowelHelper(Thai["Paiyan"], Thai["VowelUp"], line)
    cnt += cntWringVowelHelper(Thai["Paiyan"], Thai["VowelDown"], line)
    cnt += cntWringVowelHelper(Thai["Paiyan"], Thai["VowelTaiku"], line)
    cnt += cntWringVowelHelper(Thai["Paiyan"], Thai["Sound"], line)
    cnt += cntWringVowelHelper(Thai["Paiyan"], Thai["Tantakad"], line)
    cnt += cntWringVowelHelper(Thai["Paiyan"], Thai["Paiyan"], line)
    cnt += cntWringVowelHelper(Thai["Paiyan"], Thai["Yamok"], line)
               
    cnt += cntWringVowelHelper(Thai["Yamok"], Thai["VowelFront"], line)
    cnt += cntWringVowelHelper(Thai["Yamok"], Thai["VowelBack"], line)
    cnt += cntWringVowelHelper(Thai["Yamok"], Thai["VowelUm"], line)
    cnt += cntWringVowelHelper(Thai["Yamok"], Thai["VowelUp"], line)
    cnt += cntWringVowelHelper(Thai["Yamok"], Thai["VowelDown"], line)
    cnt += cntWringVowelHelper(Thai["Yamok"], Thai["VowelTaiku"], line)
    cnt += cntWringVowelHelper(Thai["Yamok"], Thai["Sound"], line)
    cnt += cntWringVowelHelper(Thai["Yamok"], Thai["Tantakad"], line)
    cnt += cntWringVowelHelper(Thai["Yamok"], Thai["Paiyan"], line)                
               
    cnt += cntWringVowelHelper(Thai["Not"], Thai["VowelBack"], line)
    cnt += cntWringVowelHelper(Thai["Not"], Thai["VowelUm"], line)
    cnt += cntWringVowelHelper(Thai["Not"], Thai["VowelUp"], line)
    cnt += cntWringVowelHelper(Thai["Not"], Thai["VowelDown"], line)
    cnt += cntWringVowelHelper(Thai["Not"], Thai["VowelTaiku"], line)
    cnt += cntWringVowelHelper(Thai["Not"], Thai["Sound"], line)
    cnt += cntWringVowelHelper(Thai["Not"], Thai["Tantakad"], line)
    
    return cnt

checkVowel = u"แโใไะาๅำัิีึืํฺุู็่้๊๋์ฯ"

def fixRepetedVowelTitle(page):
    """
    If found impossible vowel arrangement in title, 
    correct by moving that page.
    """
    opagetitle = page.title()
    pagetitle = opagetitle
    
    for i in checkVowel:
        pagetitle = lre.sub(i + u"+", i, pagetitle)
    
    if pagetitle != opagetitle:
        pywikibot.output("ย้ายบทความชื่อมีสระซ้อน")
        reason = u"โรบอต: เปลี่ยนชื่อบทความมีสระซ้อน"
        try: 
            page.move(pagetitle, reason=reason)
        except:
            wp.error()
        else:
            page = pywikibot.Page(pywikibot.getSite(), page.title())
            page.delete(reason=reason, prompt=False, mark=True)
    
def fixRepetedVowel(content):
    """If found impossible vowel arrangement in text, correct it."""
    for i in checkVowel:
        content = lre.sub(i + u"+", i, content)
    return content

'''
import random
from subprocess import Popen, PIPE, STDOUT

def randomCheckRepetition(s):
    """Helper function to check repetition of substring."""
    s = wp.toutf(s)
    s = s.replace(u"\n", u"").replace(u"", u"\n")
    size = len(s)
    begin = random.randint(0, max(0, size - 700*2))
    end = min(begin + 700*2, size)
    if not s[begin:end]:
        return 0
    p = Popen([preload.File(__file__, "rle2")],
                stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    output = p.communicate(input=s[begin:end])[0]
    return int(output)

def checkRepetition(s):
    """Check repetition of substring."""
    rnd = 3
    for i in xrange(rnd):
        res += randomCheckRepetition(s)
    return res // lim
'''
