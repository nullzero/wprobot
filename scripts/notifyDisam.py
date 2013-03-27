#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Notify user that link a link to disambiguous page."""

__version__ = "2.0.2"
__author__ = "Sorawee Porncharoenwase"

import signal
import init
import difflib
import wp
import pywikibot
from wp import ltime, lgenerator, lapi, lre
from pywikibot.data import api

def glob():
    global container, token, pagereport
    container = {}
    pagereport = pywikibot.Page(site, conf.refuselist)
    token = None

def dict2str(d):
    s = u""
    for title in d:
        s += u"; [[" + title + u"]]\n"
        s += "".join(map(lambda x: u"* [[" + x + u"]]\n", d[title]))
    return s

def notify(user, dic, insertDisamT):
    pywikibot.output(u"notifying %s..." % user)
    userobj = pywikibot.User(site, user)
    usertalk  = userobj.getUserTalkPage()
    
    refuse = False
        
    try:
        textusertalk = usertalk.get()
    except pywikibot.IsRedirectPage:
        refuse = True
    
    for title, linkset in dic.items():
        pagenow = pywikibot.Page(site, title)
        if pagenow.exists():
            alllinks = [link.title() for link in pagenow.linkedPages()]
            dic[title] = filter(lambda link: link in alllinks, list(linkset))
        else:
            dic[title] = []
            
        if not dic[title]:
            del dic[title]
            
    if not dic:
        return
    
    scontent = dict2str(dic)
    
    if ((not userobj.isRegistered()) or ('bot' in userobj.groups()) or 
                                        (not usertalk.exists()) or
                                        (conf.nonotifycat in textusertalk) or
                                        (refuse)):
        pywikibot.output("save report instead!")
        notifyreport("\n\n" + scontent)
        return
    
    message = insertDisamT
    message = message.replace(conf.linkPlaceholder, scontent)
    message = message.replace(conf.userPlaceholder, user)
    message = message.replace(conf.datePlaceholder, "%d/%d" % 
                        (ltime.date.today().day, ltime.date.today().month))
    
    try:
        usertalk.put(u"%s\n\n%s --~~~~" % (textusertalk, message),
                    conf.summary, minorEdit=False, async=True)
    except:
        wp.error()
        
    pywikibot.output(u">>> done!")

def save(user, title, links):
    pywikibot.output(u">>> save %s %s" % (user, title))
    global container
    if user in container:
        if title in container[user]:
            container[user][title] |= links
        else:
            container[user][title] = links
    else:
        container[user] = {}
        container[user][title] = links
    
def flush():
    pywikibot.output("begin flushing")
    global token, container
    token = site.token(pagereport, "edit")
    insertDisamT = pywikibot.Page(site, conf.messageTemplate).get()
    for user in container:
        notify(user, container[user], insertDisamT)
    container = {}
    pywikibot.output("end flushing")

def notifyreport(s):
    pywikibot.output("save report function!")
    if not token:
        global token
        token = site.token(pagereport, "edit")
    lapi.append(pagereport, s, conf.summary, token=token)

def check(revision):
    title = revision["title"]
    pywikibot.output(u"check page %s @ %s" % (title, wp.getTime()))
    revid = revision["revid"]
    oldrevid = revision["old_revid"]
    page = pywikibot.Page(site, title)
    textnew = page.getOldVersion(revid)
    textold = u"" if oldrevid == 0 else page.getOldVersion(oldrevid)
    
    if site.getRedirectText(textnew):
        return
    if site.getRedirectText(textold):
        textold = u""
    
    addedlinks = (set(lapi.extractLinkedPages(site, textnew, title)) -
                set(lapi.extractLinkedPages(site, textold, title)))
    disamlinks = []
    
    for link in addedlinks:
        if u":" in link.title():
            continue
        if link.title().startswith(u"#"):
            continue
        try:
            lname = link.title()
            if link.isRedirectPage():
                link = link.getRedirectTarget()
            if link.isDisambig():
                disamlinks.append(lname)
        except:
            wp.error()
    
    if len(disamlinks) != 0:
        save(revision["user"], title, set(disamlinks))
    
def main():
    def receive_signal(signum, stack):
        pywikibot.output("Flush immediately!")
        flush()
    
    signal.signal(signal.SIGUSR2, receive_signal)
        
    todaynum = ltime.date.today().day
    for rev in lgenerator.recentchanges(site,
                                        showRedirects=False,
                                        showBot=False,
                                        namespaces=conf.namespaces,
                                        repeat=True):
        try:
            check(rev)
            pywikibot.output(unicode(todaynum) + u" and " +
                             unicode(ltime.date.today().day))
            if todaynum != ltime.date.today().day:
                flush()
                todaynum = ltime.date.today().day
        except:
            wp.error()

if __name__ == "__main__":
    args, site, conf = wp.pre(u"notify linking to disambigous page",
                                    lock=True)
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
