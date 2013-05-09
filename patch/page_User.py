# -*- coding: utf-8  -*-

import init
import wp
from pywikibot.page import *
from pywikibot.data import api

def _block(self, summary, expiry=None, anon=False, noCreate=True,
           onAutoblock=True, banMail=False, allowUsertalk=True, reBlock=False,
           hidename=False):
    if self.isBlocked() and not reBlock:
        pywikibot.output("AlreadyBlocked")
        return
        #raise AlreadyBlocked()
    try:
        self.site.login(sysop=True)
    except pywikibot.NoUsername, e:
        raise NoUsername("block: Unable to login as sysop (%s)"
                    % e.__class__.__name__)
    if not self.site.logged_in(sysop=True):
        raise NoUsername("block: Unable to login as sysop")
    token = self.site.token(self, "block")
    self.site.lock_page(self)
    req = api.Request(site=self.site, action="block", token=token,
                      user=self.name(),
                      reason=summary)
    if expiry:
        req['expiry'] = expiry
    if anon:
        req['anononly'] = ""
    if noCreate:
        req['nocreate'] = ""
    if onAutoblock:
        req['autoblock'] = ""
    if banMail:
        req['noemail'] = ""
    if hidename:
        req['hidename'] = ""
    if allowUsertalk:
        req['allowusertalk'] = ""
    if reBlock:
        req['reblock'] = ""
    try:
        result = req.submit()
    except api.APIError, err:
        pywikibot.output(u"block: error code '%s' received (%s)."
                          % (err.code, unicode(err)))
        raise
    finally:
        self.site.unlock_page(self)

User.block = _block
