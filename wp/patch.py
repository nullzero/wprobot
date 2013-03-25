# -*- coding: utf-8  -*-

import pywikibot.page
import pywikibot.site

"""
========================================================================
"""
def _change_category(self, oldCat, newCat, comment=None, sortKey=None,
                    inPlace=True):
    """Remove page from oldCat and add it to newCat.

    oldCat and newCat should be Category objects.
    If newCat is None, the category will be removed.

    comment: string to use as an edit summary

    sortKey: sortKey to use for the added category.
    Unused if newCat is None, or if inPlace=True
    
    FIX: return True if succeed. Otherwise, return False.
    """
    #TODO: is inPlace necessary?
    site = self.site
    changesMade = False

    if not self.canBeEdited():
        pywikibot.output(u"Can't edit %s, skipping it..."
                          % self.title(asLink=True))
        return False
    if inPlace == True:
        newtext = pywikibot.replaceCategoryInPlace(self.text,
                                                   oldCat, newCat)
        if newtext == self.text:
            pywikibot.output(
                u'No changes in made in page %s.'
                 % self.title(asLink=True))
            return False
        try:
            self.put(newtext, comment)
            return True
        except pywikibot.EditConflict:
            pywikibot.output(
                u'Skipping %s because of edit conflict'
                 % self.title(asLink=True))
        except pywikibot.LockedPage:
            pywikibot.output(u'Skipping locked page %s'
                              % self.title(asLink=True))
        except pywikibot.SpamfilterError, error:
            pywikibot.output(
                u'Changing page %s blocked by spam filter (URL=%s)'
                             % (self.title(asLink=True), error.url))
        except pywikibot.NoUsername:
            pywikibot.output(
                u"Page %s not saved; sysop privileges required."
                             % self.title(asLink=True))
        except pywikibot.PageNotSaved, error:
            pywikibot.output(u"Saving page %s failed: %s"
                             % (self.title(asLink=True), error.message))
        return False

    # This loop will replace all occurrences of the category to be changed,
    # and remove duplicates.
    newCatList = []
    newCatSet = set()
    cats = list(self.categories(get_redirect=True))
    for i in range(len(cats)):
        cat = cats[i]
        if cat == oldCat:
            changesMade = True
            if not sortKey:
                sortKey = cat.sortKey
            if newCat:
                if newCat.title() not in newCatSet:
                    newCategory = Category(site, newCat.title(),
                                           sortKey=sortKey)
                    newCatSet.add(newCat.title())
                    newCatList.append(newCategory)
        elif cat.title() not in newCatSet:
            newCatSet.add(cat.title())
            newCatList.append(cat)

    if not changesMade:
        pywikibot.output(u'ERROR: %s is not in category %s!'
                          % (self.title(asLink=True), oldCat.title()))
    else:
        try:
            text = pywikibot.replaceCategoryLinks(self.text, newCatList)
        except ValueError:
            # Make sure that the only way replaceCategoryLinks() can return
            # a ValueError is in the case of interwiki links to self.
            pywikibot.output(
                    u'Skipping %s because of interwiki link to self' % self)
        try:
            self.put(text, comment)
            return True
        except pywikibot.EditConflict:
            pywikibot.output(
                    u'Skipping %s because of edit conflict' % self.title())
        except pywikibot.SpamfilterError, e:
            pywikibot.output(
                    u'Skipping %s because of blacklist entry %s'
                    % (self.title(), e.url))
        except pywikibot.LockedPage:
            pywikibot.output(
                    u'Skipping %s because page is locked' % self.title())
        except pywikibot.PageNotSaved, error:
            pywikibot.output(u"Saving page %s failed: %s"
                             % (self.title(asLink=True), error.message))
    return False

pywikibot.page.Page.change_category = _change_category

"""
========================================================================
"""

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
