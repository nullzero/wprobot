# -*- coding: utf-8  -*-

import init
import pywikibot.site

def _getRedirectText(self, text):
    """
    Return target of redirection. Since we obtain data from text, 
    there's no need to worry about passing section.
    """
    if hasattr(self, "patRedir"):
        m = self.patRedir.match(text)
        if m:
            return m.group(1)
        else:
            return False
    else:
        self.patRedir = self.redirectRegex()
        return self.getRedirectText(text)

pywikibot.site.APISite.getRedirectText = _getRedirectText

"""
========================================================================
"""

def _allusers(self, start="!", prefix="", group=None, onlyActive=False,
             step=None, total=None):
    from pywikibot.data import api
    augen = self._generator(api.ListGenerator, type_arg="allusers",
                                auprop="editcount|groups|registration",
                                aufrom=start, step=step, total=total)
    if prefix:
        augen.request["auprefix"] = prefix
    if group:
        augen.request["augroup"] = group
    if onlyActive:
        augen.request["auactiveusers"] = ""
    return augen

pywikibot.site.APISite.allusers = _allusers

"""
========================================================================
"""
