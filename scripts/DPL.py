# -*- coding: utf-8 -*-
"""Notify user that link a link to disambiguous page."""

__version__ = "2.0.2"
__author__ = "Sorawee Porncharoenwase"

import signal
import init
import difflib
import wp
import pywikibot
from wp import ltime, lrepeat

def glob():
    global container, pagereport
    container = {}
    pagereport = wp.Page(conf.refuselist)

def dict2str(d):
    s = u""
    for title in d:
        s += u"; [[" + title + u"]]\n"
        s += "".join(map(lambda x: u"* [[" + x + u"]]\n", d[title]))
    return s

def notify(user, dic, insertDisamT):
    for title, linkset in dic.items():
        pagenow = wp.Page(title)
        if pagenow.exists():
            alllinks = [link.title() for link in pagenow.linkedPages()]
            dic[title] = filter(lambda link: link in alllinks, list(linkset))
        else:
            dic[title] = []

        if not dic[title]:
            del dic[title]

    if not dic:
        return

    pywikibot.output("notifying %s..." % user.title())
    usertalk  = user.getUserTalkPage()

    def checkrefuse(fun):
        if not checkrefuse.val:
            checkrefuse.val |= fun()

    checkrefuse.val = False
    checkrefuse(lambda: not user.isRegistered())
    checkrefuse(lambda: not usertalk.exists())
    checkrefuse(lambda: usertalk.isRedirectPage())
    checkrefuse(lambda: "bot" in user.groups())
    checkrefuse(lambda: conf.nonotifycat in usertalk.get())

    if checkrefuse.val:
        notifyreport("\n\n" + dict2str(dic))
    else:
        try:
            lnotify.notify("dpl", usertalk, {"links": dict2str(dic)},
                           conf.summary)
        except:
            wp.error()

    pywikibot.output(">>> done!")

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
    global container
    insertDisamT = wp.Page(conf.messageTemplate).get()
    for user in container:
        try:
            notify(wp.User(user), container[user], insertDisamT)
        except:
            wp.error()
    container = {}
    pywikibot.output("end flushing")

def notifyreport(s):
    pywikibot.output("save report function!")
    pagereport.append(s, conf.summary)

def check(revision):
    title = revision["title"]
    pywikibot.output(u"check page %s @ %s" % (title, wp.getTime()))
    revid = revision["revid"]
    oldrevid = revision["old_revid"]
    page = wp.Page(title)
    textnew = page.getOldVersion(revid)
    textold = u"" if oldrevid == 0 else page.getOldVersion(oldrevid)

    if site.getRedirectText(textnew):
        return
    if site.getRedirectText(textold):
        textold = ""

    addedlinks = (set(site.pagelinks_by_text(textnew, title)) -
                set(site.pagelinks_by_text(textold, title)))
    disamlinks = []

    for link in addedlinks:
        if ":" in link.title():
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

    if disamlinks:
        save(revision["user"], title, set(disamlinks))

def main():
    def receive_signal(signum, stack):
        pywikibot.output("Flush immediately!")
        flush()

    signal.signal(signal.SIGUSR2, receive_signal)

    prevday = ltime.dt.today().day
    for rev in lrepeat.repeat(site, site.recentchanges, lambda x: x["revid"],
                              60, showRedirects=False, showBot=False,
                              changetype=["edit", "new"],
                              namespaces=conf.namespaces):
        try:
            check(rev)
        except:
            wp.error()

        if ((prevday != ltime.dt.today().day) and
                       (ltime.dt.today().day % 3 == 1)):
            try:
                flush()
            except:
                wp.error()

            prevday = ltime.dt.today().day

if __name__ == "__main__":
    args, site, conf = wp.pre("notify linking to disambigous page",
                              lock=True)
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
