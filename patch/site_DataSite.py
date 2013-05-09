# -*- coding: utf-8  -*-

import init
from pywikibot.site import *

#=======================================================================
# Support creating of item
#=======================================================================

def _editEntity(self, identification, data, bot=True, **kwargs):
    if "id" in identification and identification["id"] == "-1":
        del identification["id"]
    params = dict(**identification)
    params['action'] = 'wbeditentity'
    if bot:
        params['bot'] = 1
    if 'baserevid' in kwargs and kwargs['baserevid']:
        params['baserevid'] = kwargs['baserevid']
    params['token'] = self.token(pywikibot.Page(self, u'Main Page'), 'edit')  # Use a dummy page
    for arg in kwargs:
        if arg in ['bot', 'clear', 'data', 'exclude', 'summary']:
            params[arg] = kwargs[arg]
    params['data'] = json.dumps(data)
    req = api.Request(site=self, **params)
    data = req.submit()
    return data

DataSite.editEntity = _editEntity

def _abuselog(self, start=None, step=None, total=None, reverse=False,
              abuseid=None
             #prefix="", namespace=0, filterredir=None,
             #filterlanglinks=None, minsize=None, maxsize=None,
             #protect_type=None, protect_level=None,
             #includeredirects=None, content=False):
             ):
    apgen = self._generator(api.ListGenerator, type_arg="abuselog",
                            step=step, total=total)
    if abuseid is not None:
        apgen.request["aflfilter"] = abuseid
    if start is not None:
        apgen.request["aflstart"] = str(start)

    if reverse:
        apgen.request["afldir"] = "newer"

    return apgen

APISite.abuselog = _abuselog
