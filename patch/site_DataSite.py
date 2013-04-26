# -*- coding: utf-8  -*-

import init
from pywikibot.site import *

#=======================================================================
# Support creating of item
#=======================================================================

def _editEntity(self, identification, data, **kwargs):
    if "id" in identification and identification["id"] == "-1":
        del identification["id"]
    params = dict(**identification)
    params['action'] = 'wbeditentity'
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
