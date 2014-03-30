# -*- coding: utf-8  -*-
"""
Provide some frequently used regex.
"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import re
import pywikibot

class lre(object):
    def __init__(self, pat):
        self.regex = re.compile(pat)

    def search(self, text):
        return self.regex.search(text)

    def find(self, text, group=0):
        _x = self.search(text)
        if _x:
            return _x.group(group)
        else:
            return None

    def findall(self, text):
        return self.regex.findall(text)

    def finditer(self, text):
        return self.regex.finditer(text)

    def sub(self, subst, text):
        return self.regex.sub(subst, text)

    def subn(self, subst, text):
        return self.regex.subn(subst, text)

    def subr(self, subst, text):
        """Substitute by regex until there is no change."""
        while True:
            oldtext = text
            text = self.regex.sub(subst, text)
            if text == oldtext:
                break
        return text

    @property
    def pattern(self):
        return self.regex.pattern

class Subst(object):
    def __init__(self):
        self.all = []

    def append(self, *args):
        self.all.append((lre(args[0]), args[1], args[2:]))

    def process(self, s):
        if not isinstance(s, basestring):
            s = s.group()

        for i in self.all:
            if "subr" in i[2]:
                s = i[0].subr(i[1], s)
            else:
                s = i[0].sub(i[1], s)
        return s

def find(pat, text, group=0):
    return lre(pat).find(text, group)

def search(pat, text):
    return lre(pat).search(text)

def findall(pat, text):
    return lre(pat).findall(text)

def finditer(pat, text):
    return lre(pat).finditer(text)

def sub(pat, subst, text):
    return lre(pat).sub(subst, text)

def subn(pat, subst, text):
    return lre(pat).subn(subst, text)

def subr(pat, subst, text):
    return lre(pat).subr(subst, text)

def escape(s):
    return re.escape(s)

""" More functions! """
def genData(tagind, tag):
    return lre(u"(?s)(?<=<!-- %s%s -->).*?(?=<!-- %s%s -->)" %
                        (tagind[0], tag, tagind[1], tag))

def sep(l):
    return u"(?:" + u"|".join(l) + u")"

def getconf(key, text):
    return lre(u"(?<=<!-- %s \{).*?(?=\} -->)" % key).find(text)

def findOverlap(pattern, text):
    """Find all patterns in given text overlappingly."""
    return sum([1 for x in finditer(u"(?=(" + pattern + u"))", text) if x])

def rmsym(begin, end, text):
    return subr("(?s)%s(?:(?!%s|%s).)*%s" %
            (begin, begin, end, end), "", text)

""" More patterns! """
pats = {
    "link": lre(r"\[\[(?P<title>[^\]\|\[]*)(?P<name>\|.*?)?\]\]"),
}
