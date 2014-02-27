# -*- coding: utf-8  -*-
"""
Library to set basic environment. It also provide frequently used
function. This library should be imported in every script that require
to connect to pywikipedia library
"""

__version__ = "1.0.2"
__author__ = "Sorawee Porncharoenwase"

import sys
import os
import traceback
import init
import pywikibot
from pywikibot import config
from conf import glob as conf
from wp import ltime, lthread

def glob():
    global info
    info = {}
    info["site"] = None
    info["basescript"] = os.path.basename(sys.argv[0])
    conf.botname = os.environ["WPROBOT_BOT"]

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
    return pywikibot.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

def simplifypath(path):
    return os.path.abspath(os.path.expanduser(os.path.join(*path)))

def _login(namedict, sysop=False):
    for familyName in namedict:
        for lang in namedict[familyName]:
            site = pywikibot.getSite(code=lang, fam=familyName)
            if not (site.logged_in(sysop) and
                    site.user() == site.username(sysop)):
                site.login()

def pre(taskid=-1, lock=None, sites=[], continuous=False):
    """
    Return argument list, site object, and configuration of the script.
    This function also handles default arguments, generates lockfile
    and halt the script if lockfile exists before.
    """
    import imp
    global info
    pywikibot.handleArgs("-log")
    pywikibot.output("start task #%s at %s" % (taskid, getTime()))
    info["taskid"] = taskid
    info["lock"] = lock
    info["lockfile"] = simplifypath([os.environ["WPROBOT_DIR"], "tmp",
                                     info["basescript"] + ".lock"])
    info["continuous"] = continuous
    if os.path.exists(info["lockfile"]) and (lock != False):
        error("lockfile found. unable to execute the script.")
        pywikibot.stopme()
        sys.exit()

    open(info["lockfile"], 'w').close()

    args = pywikibot.handleArgs() # must be called before getSite()
    site = pywikibot.getSite()
    info["site"] = site
    
    """
    if sites == True:
        _login(config.usernames)
        _login(config.sysopnames, sysop=True)
    else:
        _login({site.family.name: {site.code: None}})
        for isite in sites:
            _login({isite.family.name: {isite.code: None}})
    """

    confpath = simplifypath([os.environ["WPROBOT_DIR"], "conf",
                            info["basescript"]])

    module = (imp.load_source("conf", confpath) if os.path.exists(confpath)
                                                else None)
    return args, site, module

def run(func):
    global info
    task = ReadCode(Page(u"User:Nullzerobot/แผงควบคุม"), "task")
    task.load()

    if info["taskid"] not in task.data:
        func()
        return

    if not task.data[info["taskid"]]:
        ltime.sleep(3 * 60 * 60) # sleep 3 hours
        return

    thread = lthread.EThread(target=func)
    thread.daemon = True
    thread.start()

    try:
        while True:
            for i in xrange(12):
                if not thread.isAlive():
                    break
                ltime.sleep(5)

            task.load()
            if not (task.data[info["taskid"]] and thread.isAlive()):
                break
    except:
        error()

    if thread.error:
        raise RuntimeError

def post(unlock=True):
    """
    This function removes throttle file. It also removes lockfile unless
    unlock variable is set to False
    """
    if unlock or (not info["lock"]):
        try:
            os.remove(info["lockfile"])
        except OSError:
            error("unable to remove lockfile.")
    pywikibot.output("stop task at " + getTime())
    pywikibot.stopme()

def posterror():
    """This function forces program stop without removing lockfile"""
    try:
        error()
    except (KeyboardInterrupt, SystemExit):
        post()
        sys.exit()
    else:
        error("suddenly halt!")
        post(unlock=False)
    if info["continuous"]:
        raise RuntimeError

def handlearg(start, arg):
    """This function determines whether the specified argument matches
    required name. If a list is sent, the function will check all 
    elements and return the first matching"""
    if isinstance(arg, list):
        for item in arg:
            result = handlearg(start, item)
            if result is not None:
                return toutf(result)
        return None
    if arg == "-" + start:
        return True
    if arg.startswith("-" + start + ":"):
        return arg[2 + len(start):]
    else:
        return None

"""
Shortcut function.
"""

def Page(title):
    global info
    if not info["site"]:
        info["site"] = pywikibot.getSite()
    return pywikibot.Page(info["site"], title)

def User(title):
    global info
    if not info["site"]:
        info["site"] = pywikibot.getSite()
    return pywikibot.User(info["site"], title)

def Category(title):
    global info
    if not info["site"]:
        info["site"] = pywikibot.getSite()
    return pywikibot.Category(info["site"], title)

glob()

class ReadCode(object):
    def __init__(self, page, var):
        self.page = page
        self.var = var
        self.data = {}

    def load(self):
        locals()[self.var] = {}
        exec("\n".join(self.page.get(force=True).splitlines()[1:-1]))
        self.data = locals()[self.var]
