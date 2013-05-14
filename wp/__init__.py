# -*- coding: utf-8  -*-
"""
Library to set basic environment. It also provide frequently used
function. This library should be imported in every script that require
to connect to pywikipedia library
"""

__version__ = "1.0.2"
__author__ = "Sorawee Porncharoenwase"

import init
import sys
import os
import traceback
import datetime
import time
import pywikibot
from pywikibot import config
from conf import glob as conf

def glob():
    global basescript, fullname, lockfile, site
    conf.botname = os.environ["WPROBOT_BOT"]
    basescript = os.path.basename(sys.argv[0])
    fullname = None
    lockfile = None
    site = None

def tostr(st):
    """Return normal quoted string."""
    if not st:
        return None
    try:
        st = str(st)
    except UnicodeEncodeError:
        st = st.encode("utf-8")
    return st

def toutf(st):
    """Return unicode quoted string."""
    if not st:
        return None
    try:
        st = unicode(st)
    except UnicodeDecodeError:
        st = st.decode("utf-8")
    return st

def error(e=None):
    """
    If error message is given, print that error message. Otherwise,
    print traceback instead.
    """
    if e:
        pywikibot.output("E: " + e)
    else:
        exc = sys.exc_info()[0]
        if (exc == KeyboardInterrupt) or (exc == SystemExit):
            sys.exit()
        pywikibot.output("E: " + toutf(traceback.format_exc()))

def getTime():
    """Print timestamp."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def simplifypath(path):
    return os.path.abspath(os.path.expanduser(os.path.join(*path)))

def _login(namedict, sysop=False):
    for familyName in namedict:
        for lang in namedict[familyName]:
            site = pywikibot.getSite(code=lang, fam=familyName)
            if not (site.logged_in(sysop) and
                    site.user() == site.username(sysop)):
                site.login()

def pre(name, lock=False, sites=[]):
    """
    Return argument list, site object, and configuration of the script.
    This function also handles default arguments, generates lockfile
    and halt the script if lockfile exists before.
    """
    import imp
    global site
    args = pywikibot.handleArgs() # must be called before getSite()
    site = pywikibot.getSite()
    
    if sites == True:
        _login(config.usernames)
        _login(config.sysopnames, sysop=True)
    else:
        _login({site.family.name: {site.code: None}})
        for isite in sites:
            _login({isite.family.name: {isite.code: None}})

    global fullname, lockfile
    pywikibot.handleArgs("-log")
    fullname = name
    pywikibot.output(">>> " + fullname + " <<< Start # " + getTime())
    if lock:
        lockfile = simplifypath([os.environ["WPROBOT_DIR"], "tmp",
                                basescript + ".lock"])
        if os.path.exists(lockfile):
            error("Lockfile found. Unable to execute the script.")
            pywikibot.stopme()
            time.sleep(60*60*3)
            sys.exit()
        open(lockfile, 'w').close()

    confpath = simplifypath([os.environ["WPROBOT_DIR"], "conf",
                                basescript])
    if os.path.exists(confpath):
        module = imp.load_source("conf", confpath)
    else:
        module = None
    return args, site, module

def post(unlock=True):
    """
    This function removes throttle file. It also removes lockfile unless
    unlock variable is set to False
    """
    if unlock and lockfile:
        try:
            os.remove(lockfile)
        except OSError:
            error("Unable to remove lockfile.")

    pywikibot.output(">>> " + fullname + " <<< Stop # " + getTime())
    pywikibot.stopme()
    sys.exit()

def posterror():
    """This function forces program stop without removing lockfile"""
    error()
    error(u"Suddenly halt!")
    post(unlock = False)

def handlearg(start, arg):
    if arg.startswith("-" + start + ":"):
        return arg[2 + len(start):]
    else:
        return None

"""
Shortcut function.
"""

def Page(title):
    global site
    if not site:
        site = pywikibot.getSite()
    return pywikibot.Page(site, title)

def User(title):
    global site
    if not site:
        site = pywikibot.getSite()
    return pywikibot.User(site, title)

def Category(title):
    global site
    if not site:
        site = pywikibot.getSite()
    return pywikibot.Category(site, title)

glob()
