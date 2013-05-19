#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Service to move category automatically. There are two modes in running;
major and minor.

Major mode will look for each request at pageMajor and perform it if
requester passes qualification. If not, the script will append that
request to pageMinor. This mode should be executed periodically.

Minor mode will perform every request in pageMinor without qualifying.
This mode should be executed manually and deliberately. It can be
activated by running script with parameter "pending"
(can use alternative word by changing variable 'pendingParam')

Requirement:
    servicePath:    Main page's prefix
    pageMajor:      Page that customer will leave their requests.
    pageMinor:      Page that unqualified automatically request will
                    be kept.
    datwiki:        Page that keep id of last revision. To prevent
                    vandalism on this page, the page should be local
                    javascript (end with .js) so that there are only
                    page owner and administrator that can change that
                    page.

    Don't give fullpath to pageMajor, pageMinor, and datwiki! The script
    will obtain the actual path by concatenating servicePath's value and
    their values together.

    minEditCount:   Edit count constraint for qualifying user.
    minTime:        Membership duration constraint for qualifying user.
"""

__version__ = "2.0.1"
__author__ = "Sorawee Porncharoenwase"

import itertools
import init
import wp
import pywikibot
from wp import lservice, lre, lthread, ltime
from pywikibot import i18n

"""
Following codes are copied from Pywikipedia and are extent to support
multithreading.
"""

def copyAndKeep(oldcat, catname):
    """
    Returns true if copying was successful, false if target page already
    existed.
    """
    result = True
    targetCat = pywikibot.Page(oldcat.site, catname, ns=14)
    if targetCat.exists():
        result = False
        pywikibot.output('Target page %s already exists!' % targetCat.title())
    else:
        pywikibot.output('Moving text from %s to %s.' %
                        (oldcat.title(), targetCat.title()))

        targetCat.put(oldcat.get(), u'โรบอต: ย้ายจาก %s. ผู้ร่วมเขียน: %s' %
                     (oldcat.title(), ', '.join(oldcat.contributingUsers())))

    item = pywikibot.ItemPage.fromPage(oldcat)
    testitem = pywikibot.ItemPage.fromPage(targetCat)
    pywikibot.output("debug: oldcat %s and newcat %s" %
                    (str(item.exists()), str(testitem.exists())))
    if not testitem.exists() and item.exists():
        item.editEntity({'sitelinks': {site.dbName(): {'site': site.dbName(),
                                                'title': targetCat.title()}},
                         'labels': {site.code: {'language': site.code,
                                                'value': targetCat.title()}}})
    return result

class CategoryMoveRobot:
    """Robot to move pages from one category to another."""

    def __init__(self, oldCatTitle, newCatTitle):
        self.site = site
        self.oldCat = pywikibot.Category(self.site, oldCatTitle)
        self.newCatTitle = newCatTitle

    def run(self):
        newCat = pywikibot.Category(self.site, self.newCatTitle)
        reason = i18n.twtranslate(self.site, 'category-was-moved') \
                     % {'newcat': self.newCatTitle, 'title': self.newCatTitle}

        self.editSummary = i18n.twtranslate(site, 'category-changing') \
                               % {'oldcat':self.oldCat.title(),
                                  'newcat':newCat.title()}

        copied = False
        oldMovedTalk = None
        if self.oldCat.exists():
            copied = copyAndKeep(self.oldCat, self.newCatTitle)
            if copied:
                oldTalk = self.oldCat.toggleTalkPage()
                if oldTalk.exists():
                    newTalkTitle = newCat.toggleTalkPage().title()
                    try:
                        talkMoved = oldTalk.move(newTalkTitle, reason)
                    except (pywikibot.NoPage, pywikibot.PageNotSaved), e:
                        #in order :
                        #Source talk does not exist, or
                        #Target talk already exists
                        pywikibot.output(e.message)
                    else:
                        if talkMoved:
                            oldMovedTalk = oldTalk

        pool = lthread.ThreadPool(30)

        def localchange(article, oldCat, newCat, comment):
            if ((not article.change_category(oldCat, newCat, comment)) and
                     article.namespace() in wp.conf.nstl):
                pagedoc = wp.Page(article.title() + "/doc")
                if pagedoc.exists():
                    pagedoc.change_category(oldCat, newCat, comment)

        for article in itertools.chain(self.oldCat.articles(),
                                       self.oldCat.subcategories()):
            pool.add_task(localchange, article, self.oldCat,
                        newCat, self.editSummary)

        pool.wait_completion()
        # Delete the old category and its moved talk page
        if copied:
            ltime.sleep(15)
            if self.oldCat.isEmptyCategory():
                self.oldCat.delete(reason, prompt=False,
                                   mark=True, blank=True)
                if oldMovedTalk is not None:
                    oldMovedTalk.delete(reason, prompt=False,
                                        mark=True, blank=True)
            else:
                pywikibot.output('Couldn\'t delete %s - not empty.'
                                 % self.oldCat.title())
        site.login()

def glob():
    lre.pats["name"] = lre.lre(r"\[\[:.*?:(.*?)\]\]")
    # strip namespace in order to i18n properly
    lre.pats["endtable"] = lre.lre(ur"(?m)^\|\}")

def summaryWithTime():
    return conf.summary + " @ " + wp.getTime()

def domove(source, dest):
    """
    To move a category. If bot hasn't administrator privilege,
    it will tag speedydelete tag and clear content to prevent
    interwikibot add interwiki link wrongly.
    """
    pywikibot.output(u"Move from " + source + u" to " + dest)
    robot = CategoryMoveRobot(source, dest)
    robot.run()

def verify(name):
    """Verify a username whether he is reliable."""
    user = pywikibot.User(site, name)
    return (user.isRegistered() and (user.editCount() >= conf.minEditCount) and
           (not user.isBlocked()) and ((user.registration() is None) or
           (site.getcurrenttime() - user.registration()).days >= conf.minTime))

def appendTable(title, arr):
    """Append data to a table."""
    if not arr:
        return
    page = wp.Page(title)
    page.put(lre.pats["endtable"].sub("\n".join(arr) + "\n|}", page.get()),
             summaryWithTime())

def main():
    """Main function"""
    if conf.pendingParam in args:
        pywikibot.output("move pending entry")
        title = conf.pageMinor
        operation = "minor"
    else:
        title = conf.pageMajor
        operation = "major"

    header, table, disable = lservice.service(page=wp.Page(title),
                                              confpage=wp.Page(conf.datwiki),
                                              operation=operation,
                                              verify=verify,
                                              summary=summaryWithTime,
                                              #debug=True,
                                              )

    report = []
    pending = []

    for i, line in enumerate(table):
        putline = "|-\n| " + " || ".join(line)
        if (operation == "minor") or (not disable[i]):
            templateStat = conf.notDoneTemplate

            try:
                domove(lre.pats["name"].find(line[1], 1),
                       lre.pats["name"].find(line[2], 1))
            except:
                wp.error()
            else:
                templateStat = conf.doneTemplate

            putline += " || %s %s" % (templateStat, wp.getTime())
            report.append(putline)
        else:
            pending.append(putline)

    appendTable(conf.pageReport, report)
    appendTable(conf.pageMinor, pending)

if __name__ == "__main__":
    sites = [pywikibot.getSite("wikidata", "wikidata")]
    args, site, conf = wp.pre(-1, lock=True, sites=sites)
    try:
        glob()
        wp.run(main)
    except:
        wp.posterror()
    else:
        wp.post()
