# -*- coding: utf-8  -*-

import init
import wp
from pywikibot.page import *
from pywikibot.data import api
from pywikibot.tools import (
    ComparableMixin, deprecated, deprecate_arg, deprecated_args
)
from wp import ltime
from wp import lre

#=======================================================================
# add fromtext in order to find including of explicitly category
#=======================================================================
from pywikibot.page import Page

@deprecate_arg("nofollow_redirects", None)
@deprecate_arg("get_redirect", None)
def _categories(self, withSortKey=False, step=None, total=None,
               content=False, fromtext=False):
    """Iterate categories that the article is in.

    @param withSortKey: if True, include the sort key in each Category.
    @param step: limit each API call to this number of pages
    @param total: iterate no more than this number of pages in total
    @param content: if True, retrieve the content of the current version
        of each category description page (default False)
    @return: a generator that yields Category objects.

    """
    if fromtext:
        return pywikibot.getCategoryLinks(self.get(), self.site)
    return self.site.pagecategories(self, withSortKey=withSortKey,
                                    step=step, total=total, content=content)
Page.categories = _categories

#=======================================================================
# NEW: getLang
#=======================================================================

def _getLang(self, site):
    for link in self.langlinks():
        if link.site == site:
            if self.__class__ == pywikibot.Page:
                return self.__class__(link.site, link.title, ns=link.namespace)
            else:
                return self.__class__(link.site, link.title)
            # To support inheritance class

Page.getLang = _getLang

#=======================================================================
# NEW: append
#=======================================================================

def _append(self, *args, **kwargs):
    if kwargs.pop('async', False):
        pywikibot.async_request(self.site.appendpage, self, *args, **kwargs)
    else:
        self.site.appendpage(self, *args, **kwargs)

Page.append = _append

'''
#=======================================================================
# NEW: _helper
#=======================================================================

def _helper(page, data, inPlace, noInclude=False):
    def multiline(arr):
        return "\n".join(["[[" + i.title() + "]]" for i in arr])

    if not inPlace:
        page.text = pywikibot.replaceCategoryLinks(page.text, data)
        return

    if noInclude:
        if "<noinclude>" in page.text:
            page.text = lre.sub_last("<noinclude>", "<noinclude>\n" +
                                     multiline(data), page.text)
        else:
            page.text += "<noinclude>\n" + multiline(data) + "\n</noinclude>"
        return

    lre.pats["cat"] = (lre.lre(r"(?i)\[\[\s*(%s)\s*:.*?\]\]" %
                       "|".join(page.site.category_namespaces())))



#=======================================================================
# NEW: add_category
#=======================================================================

def _add_category(self, cats, inPlace=False):
    inPlace = inPlace or (self.namespace() in wp.conf.nstl)
    old = set(self.categories(fromtext=True))
    new = set(cats)
    if old + new == old:
        pywikibot.output("Add category: Nothing change!")
        return False
    _helper(self, list(old + new), inPlace, len(old) == 0)
    return True

#=======================================================================
# remove_category
#=======================================================================

def _remove_category(self, cats, inPlace=False):
    inPlace = inPlace or (self.namespace() in wp.conf.nstl)
    old = set(self.categories(fromtext=True))
    new = set(cats)
    if old - new == old:
        pywikibot.output("Remove category: Nothing change!")
        return False
    _helper(self, list(old - new), inPlace)
    return True

#=======================================================================
# change_category
#=======================================================================

def _change_category2(self, oldCat, newCat, inPlace=False):
    inPlace = inPlace or (self.namespace() in wp.conf.nstl)
    if oldCat == newCat:
        pywikibot.output("Change category: Nothing change!")
        return False
    old = set(self.categories(fromtext=True))
    if oldCat not in old:
        pywikibot.output("Change category: Nothing change!")
        return False
    self.add_category(newCat, inPlace)
    self.remove_category(oldCat, inPlace)
    return True
'''

#=======================================================================
# NEW: add_category
#=======================================================================

def _add_category(self, cats):
    old = set(self.categories(fromtext=True))
    new = set(cats)
    if old | new == old:
        pywikibot.output("Add category: Nothing change!")
        return False
    self.put(pywikibot.replaceCategoryLinks(self.get(), list(old | new), self.site),
             u"เพิ่มหมวดหมู่")
    return True

Page.add_category = _add_category

#=======================================================================
# NEW: parentPage
#=======================================================================

def _parentPage(self, level=1):
    title = self.title()
    while(level > 0):
        title, occ = lre.subn("/[^/]*$", "", title)
        if occ == 0: break
        level -= 1
    return Page(title)

Page.parentPage = _parentPage