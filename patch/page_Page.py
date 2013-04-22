# -*- coding: utf-8  -*-

import init
import wp
from pywikibot.page import *
from pywikibot.data import api
from wp import ltime

#=======================================================================
# Change position of initializing revision dict in order to prevent
# error when putting
#=======================================================================

def ___init__(self, source, title=u"", ns=0):
    """Instantiate a Page object.

    Three calling formats are supported:

      - If the first argument is a Page, create a copy of that object.
        This can be used to convert an existing Page into a subclass
        object, such as Category or ImagePage.  (If the title is also
        given as the second argument, creates a copy with that title;
        this is used when pages are moved.)
      - If the first argument is a Site, create a Page on that Site
        using the second argument as the title (may include a section),
        and the third as the namespace number. The namespace number is
        mandatory, even if the title includes the namespace prefix. This
        is the preferred syntax when using an already-normalized title
        obtained from api.php or a database dump.  WARNING: may produce
        invalid objects if page title isn't in normal form!
      - If the first argument is a Link, create a Page from that link.
        This is the preferred syntax when using a title scraped from
        wikitext, URLs, or another non-normalized source.

    @param source: the source of the page
    @type source: Link, Page (or subclass), or Site
    @param title: normalized title of the page; required if source is a
        Site, ignored otherwise
    @type title: unicode
    @param ns: namespace number; required if source is a Site, ignored
        otherwise
    @type ns: int

    """
    self._revisions = {} # >>HERE<<
    if isinstance(source, pywikibot.site.BaseSite):
        self._link = Link(title, source=source, defaultNamespace=ns)
    elif isinstance(source, Page):
        # copy all of source's attributes to this object
        self.__dict__ = source.__dict__
        if title:
            # overwrite title
            self._link = Link(title, source=source.site, defaultNamespace=ns)
    elif isinstance(source, Link):
        self._link = source
    else:
        raise pywikibot.Error(
              "Invalid argument type '%s' in Page constructor: %s"
              % (type(source), source))

Page.__init__ = ___init__

#=======================================================================
# return status of completion
#=======================================================================

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
        else:
            return True # >>HERE<<
    return False

Page.change_category = _change_category

#=======================================================================
# Support blank and mark parameter
#=======================================================================

def _delete(self, reason=None, prompt=True, throttle=None,
            mark=False, blank=False):
    """Deletes the page from the wiki. Requires administrator status.

    @param reason: The edit summary for the deletion. If None, ask for it.
    @param prompt: If true, prompt user for confirmation before deleting.
    @param mark: if true, and user does not have sysop rights, place a
        speedy-deletion request on the page instead.

    """
    # TODO: add support for mark
    if reason is None:
        pywikibot.output(u'Deleting %s.' % (self.title(asLink=True)))
        reason = pywikibot.input(u'Please enter a reason for the deletion:')
    answer = u'y'
    if prompt and not hasattr(self.site, '_noDeletePrompt'):
        answer = pywikibot.inputChoice(u'Do you want to delete %s?'
                    % self.title(asLink = True, forceInterwiki = True),
                                       ['Yes', 'No', 'All'],
                                       ['Y', 'N', 'A'],
                                       'N')
        if answer in ['a', 'A']:
            answer = 'y'
            self.site._noDeletePrompt = True
    if answer in ['y', 'Y']:
        try:
            return self.site.deletepage(self, reason)
        except pywikibot.NoUsername, e:
            if mark: # >>HERE<<
                text = self.get(get_redirect=True)
                self.put(u'{{speedydelete|1=%s --~~~~|bot=yes}}\n\n%s' %
                        (reason, "" if blank else text), comment=reason)
            else:
                raise e

Page.delete = _delete

#=======================================================================
# add onlyInclude in order to find including of explicitly category
#=======================================================================

def _categories(self, withSortKey=False, step=None, total=None,
               content=False, onlyInclude=False):
    """Iterate categories that the article is in.

    @param withSortKey: if True, include the sort key in each Category.
    @param step: limit each API call to this number of pages
    @param total: iterate no more than this number of pages in total
    @param content: if True, retrieve the content of the current version
        of each category description page (default False)
    @return: a generator that yields Category objects.

    """
    if onlyInclude: # >>HERE<<
        return pywikibot.getCategoryLinks(self.get(), self.site)
    else:
        return self.site.pagecategories(self, withSortKey=withSortKey,
                                    step=step, total=total, content=content)

Page.categories = _categories

########################################################################
########################################################################
########################################################################

#=======================================================================
# get other language page
#=======================================================================

def _getLang(self, site):
    for link in self.langlinks():
        if link.site == site:
            return self.__class__(link.site, link.title)

Page.getLang = _getLang

#=======================================================================
# append text to a page
#=======================================================================

def _append(self, text, comment="", minorEdit=True, botflag=True,
           async=False, nocreate=True):
    # TODO: async support
    token = self.site.token(self, "edit")
    #token = page.site.getToken("edit")
    r = api.Request(site=self.site, action="edit", title=self.title(),
                    appendtext=text, summary=comment, token=token)

    if minorEdit:
        r["minor"] = ""

    if botflag:
        r["bot"] = ""

    if nocreate:
        r["nocreate"] = ""

    try:
        r.submit()
    except:
        wp.error()

Page.append = _append

#=======================================================================
# implement protect
#=======================================================================

def _protect(self, summary, locktype=None, duration=None, level=None):
    if duration is None or isinstance(duration, basestring):
        expiry = duration
    else:
        expiry = self.site.getcurrenttime() + ltime.td(**duration)
    level = level or "sysop"
    locktype = locktype or "edit"
    try:
        self.site.login(sysop=True)
    except pywikibot.NoUsername, e:
        raise NoUsername("protect: Unable to login as sysop (%s)"
                    % e.__class__.__name__)
    if not self.site.logged_in(sysop=True):
        raise NoUsername("protect: Unable to login as sysop")
    token = self.site.token(self, "protect")
    self.site.lock_page(self)
    req = api.Request(site=self.site, action="protect", token=token,
                      title=self.title(withSection=False),
                      reason=summary, protections=locktype+"="+level)
    if expiry:
        req["expiry"] = expiry
    try:
        result = req.submit()
    except api.APIError, err:
        errdata = {
            'site': self.site,
            'title': self.title(withSection=False),
            'user': self.site.user(),
        }
        pywikibot.output(u"protect: error code '%s' received (%s)."
                          % (err.code, unicode(errdata)))
        raise
    finally:
        self.site.unlock_page(self)

Page.protect = _protect
