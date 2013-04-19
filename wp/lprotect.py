# -*- coding: utf-8  -*-

import init
from wp import ltime
from pywikibot.data import api

def protect(site, page, summary, locktype=None, period=None, level=None):
    if period is None or isinstance(period, basestring):
        expiry = period
    else:
        expiry = site.getcurrenttime() + ltime.td(**period)
    level = level or "sysop"
    locktype = locktype or "edit"
    try:
        site.login(sysop=True)
    except pywikibot.NoUsername, e:
        raise NoUsername("protect: Unable to login as sysop (%s)"
                    % e.__class__.__name__)
    if not site.logged_in(sysop=True):
        raise NoUsername("protect: Unable to login as sysop")
    token = site.token(page, "protect")
    site.lock_page(page)
    req = api.Request(site=site, action="protect", token=token,
                      title=page.title(withSection=False),
                      reason=summary, protections=locktype+"="+level)
    if expiry:
        req["expiry"] = expiry
    try:
        result = req.submit()
    except api.APIError, err:
        errdata = {
            'site': site,
            'title': page.title(withSection=False),
            'user': site.user(),
        }
        pywikibot.output(u"protect: error code '%s' received (%s)."
                          % (err.code, unicode(errdata)))
        raise
    finally:
        site.unlock_page(page)
