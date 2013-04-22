# -*- coding: utf-8  -*-

import init
from pywikibot.page import *

#=======================================================================
# Support creating of item
#=======================================================================

def ___defined_by(self, singular=False):
    """
    returns the parameters needed by the API to identify an item.
    Once an item's "p/q##" is looked up, that will be used for all future
    requests.
    @param singular: Whether the parameter names should use the singular
                     form
    @type singular: bool
    """
    params = {}
    if singular:
        id = 'id'
        site = 'site'
        title = 'title'
    else:
        id = 'ids'
        site = 'sites'
        title = 'titles'
    #id overrides all
    if hasattr(self, 'id'):
        if self.id != "-1": # >>HERE<<
            params[id] = self.id
        return params

    #the rest only applies to ItemPages, but is still needed here.

    if isinstance(self.site, pywikibot.site.DataSite):
        params[id] = self.title(withNamespace=False)
    elif isinstance(self.site, pywikibot.site.BaseSite):
        params[site] = self.site.dbName()
        params[title] = self.title()
    else:
        raise pywikibot.exceptions.BadTitle
    return params

WikibasePage.__defined_by = ___defined_by
