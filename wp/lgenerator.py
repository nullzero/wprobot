# -*- coding: utf-8  -*-

__version__ = "1.0.2"
__author__ = "Sorawee Porncharoenwase"

import time
import init
import pywikibot
from wp import ltime
from pywikibot.data import api

def recentchanges(site, start=None, end=None, reverse=False,
                  namespaces=None, pagelist=None, changetype=None,
                  showMinor=None, showBot=None, showAnon=None,
                  showRedirects=None, showPatrolled=None, topOnly=False,
                  step=None, total=None, repeat=False):
    """Iterate recent changes.

    @param start: Timestamp to start listing from
    @param end: Timestamp to end listing at
    @param reverse: if True, start with oldest changes (default: newest)
    @param pagelist: iterate changes to pages in this list only
    @param pagelist: list of Pages
    @param changetype: only iterate changes of this type ("edit" for
        edits to existing pages, "new" for new pages, "log" for log
        entries)
    @param showMinor: if True, only list minor edits; if False (and not
        None), only list non-minor edits
    @param showBot: if True, only list bot edits; if False (and not
        None), only list non-bot edits
    @param showAnon: if True, only list anon edits; if False (and not
        None), only list non-anon edits
    @param showRedirects: if True, only list edits to redirect pages; if
        False (and not None), only list edits to non-redirect pages
    @param showPatrolled: if True, only list patrolled edits; if False
        (and not None), only list non-patrolled edits
    @param topOnly: if True, only list changes that are the latest revision
        (default False)

    """
    if repeat:
        reverse = True
        start = start or site.getcurrenttimestamp()
        
    seen = set()
    while True:
        if start and end:
            if reverse:
                if end < start:
                    raise Error(
            "recentchanges: end must be later than start with reverse=True")
            else:
                if start < end:
                    raise Error(
            "recentchanges: start must be later than end with reverse=False")
        rcgen = site._generator(api.ListGenerator, type_arg="recentchanges",
                                rcprop="user|comment|timestamp|title|ids"
                                       "|sizes|redirect|loginfo"
                                       #"|sizes|redirect|patrolled|loginfo" - patrol rights needed
                                       "|flags",
                                namespaces=namespaces, step=step,
                                total=total)
        if start is not None:
            rcgen.request["rcstart"] = str(start)
        if end is not None:
            rcgen.request["rcend"] = str(end)
        if reverse:
            rcgen.request["rcdir"] = "newer"
        if pagelist:
            if site.versionnumber() > 14:
                pywikibot.warning(
                    u"recentchanges: pagelist option is disabled; ignoring.")
            else:
                rcgen.request["rctitles"] = u"|".join(p.title(withSection=False)
                                                      for p in pagelist)
        if changetype:
            rcgen.request["rctype"] = changetype
        if topOnly:
            rcgen.request["rctoponly"] = ""
        filters = {'minor': showMinor,
                   'bot': showBot,
                   'anon': showAnon,
                   'redirect': showRedirects,}
                   #'patrolled': showPatrolled}
        rcshow = []
        for item in filters:
            if filters[item] is not None:
                rcshow.append(filters[item] and item or ("!"+item))
        if rcshow:
            rcgen.request["rcshow"] = "|".join(rcshow)
        
        for ipage in rcgen:
            if ipage['revid'] not in seen:
                seen.add(ipage['revid'])
                yield ipage
                
        if not repeat:
            break
        
        time.sleep(24)
        start = ltime.timestampdelta(site.getcurrenttimestamp(), -30)
