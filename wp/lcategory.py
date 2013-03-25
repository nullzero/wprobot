# -*- coding: utf-8  -*-
"""
Mangage category
"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import init
import pywikibot
from pywikibot import catlib

def change_category(article, oldCat, newCat, comment=None, sortKey=None,
                    inPlace=False):
    """
    Given an article which is in category oldCat, moves it to
    category newCat. Moves subcategories of oldCat as well.
    oldCat and newCat should be Category objects.
    If newCat is None, the category will be removed.
    """
    cats = article.categories(get_redirect=True)
    site = article.site()
    changesMade = False

    if not article.canBeEdited():
        pywikibot.output("Can't edit %s, skipping it..."
                         % article.title(asLink=True))
        return False
    if inPlace or article.namespace() == 10:
        oldtext = article.get(get_redirect=True)
        newtext = pywikibot.replaceCategoryInPlace(oldtext, oldCat, newCat)
        if newtext == oldtext:
            pywikibot.output(
                u'No changes in made in page %s.' % article.title(asLink=True))
            return False
        try:
            article.put(newtext, comment)
            return True
        except pywikibot.EditConflict:
            pywikibot.output(u'Skipping %s because of edit conflict'
                             % article.title(asLink=True))
        except pywikibot.LockedPage:
            pywikibot.output(u'Skipping locked page %s'
                             % article.title(asLink=True))
        except pywikibot.SpamfilterError, error:
            pywikibot.output(u'Changing page %s blocked by spam filter (URL=%s)'
                             % (article.title(asLink=True), error.url))
        except pywikibot.NoUsername:
            pywikibot.output(u'Page %s not saved; sysop privileges required.'
                             % article.title(asLink=True))
        except pywikibot.PageNotSaved, error:
            pywikibot.output(u'Saving page %s failed: %s'
                             % (article.title(asLink=True), error.message))
        return False

    # This loop will replace all occurrences of the category to be changed,
    # and remove duplicates.
    newCatList = []
    newCatSet = set()
    for i in range(len(cats)):
        cat = cats[i]
        if cat == oldCat:
            changesMade = True
            if not sortKey:
                sortKey = cat.sortKey
            if newCat:
                if newCat.title() not in newCatSet:
                    newCategory = catlib.Category(site, newCat.title(),
                                           sortKey=sortKey)
                    newCatSet.add(newCat.title())
                    newCatList.append(newCategory)
        elif cat.title() not in newCatSet:
            newCatSet.add(cat.title())
            newCatList.append(cat)

    if not changesMade:
        pywikibot.output(u'ERROR: %s is not in category %s!'
                         % (article.title(asLink=True), oldCat.title()))
    else:
        text = article.get(get_redirect=True)
        try:
            text = pywikibot.replaceCategoryLinks(text, newCatList)
        except ValueError:
            # Make sure that the only way replaceCategoryLinks() can return
            # a ValueError is in the case of interwiki links to self.
            pywikibot.output(
                    u'Skipping %s because of interwiki link to self' % article)
        try:
            article.put(text, comment)
            return True
        except pywikibot.EditConflict:
            pywikibot.output(
                    u'Skipping %s because of edit conflict' % article.title())
        except pywikibot.SpamfilterError, e:
            pywikibot.output(
                    u'Skipping %s because of blacklist entry %s'
                    % (article.title(), e.url))
        except pywikibot.LockedPage:
            pywikibot.output(
                    u'Skipping %s because page is locked' % article.title())
        except pywikibot.PageNotSaved, error:
            pywikibot.output(u"Saving page %s failed: %s"
                             % (article.title(asLink=True), error.message))
    return False
