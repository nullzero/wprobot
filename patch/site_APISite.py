# -*- coding: utf-8  -*-

import init
from pywikibot.site import *
import wp
from wp import ltime, lre

_logger = "wiki.site"

#=======================================================================
# Support for onlyActive parameter
#=======================================================================

def _allusers(self, start="!", prefix="", group=None, onlyActive=False,
             step=None, total=None):
    augen = self._generator(api.ListGenerator, type_arg="allusers",
                                auprop="editcount|groups|registration",
                                aufrom=start, step=step, total=total)
    if prefix:
        augen.request["auprefix"] = prefix
    if group:
        augen.request["augroup"] = group
    if onlyActive: # >>HERE<<
        augen.request["auactiveusers"] = ""
    return augen

APISite.allusers = _allusers

#=======================================================================
'''
@must_be(group='user')
def _editpage(self, page, summary, minor=True, notminor=False,
             bot=True, recreate=True, createonly=False, watch=None):
    """Submit an edited Page object to be saved to the wiki.

    @param page: The Page to be saved; its .text property will be used
        as the new text to be saved to the wiki
    @param token: the edit token retrieved using Site.token()
    @param summary: the edit summary (required!)
    @param minor: if True (default), mark edit as minor
    @param notminor: if True, override account preferences to mark edit
        as non-minor
    @param recreate: if True (default), create new page even if this
        title has previously been deleted
    @param createonly: if True, raise an error if this title already
        exists on the wiki
    @param watch: Specify how the watchlist is affected by this edit, set
        to one of "watch", "unwatch", "preferences", "nochange":
        * watch: add the page to the watchlist
        * unwatch: remove the page from the watchlist
        * preferences: use the preference settings (Default)
        * nochange: don't change the watchlist
    @param botflag: if True, mark edit with bot flag
    @return: True if edit succeeded, False if it failed

    """
    text = page.text
    if not text:
        raise Error("editpage: no text to be saved")
    if hasattr(page, "_revid"):
        lastrev = page._revid
    else:
        lastrev = None
    token = self.getToken("edit")
    self.lock_page(page)
    params = dict(action="edit",
                  title=page.title(withSection=False),
                  text=text, token=token, summary=summary)
    if bot:
        params["bot"] = ""
    if lastrev is not None:
        params["basetimestamp"] = page._revisions[lastrev].timestamp
    if minor:
        params['minor'] = ""
    elif notminor:
        params['notminor'] = ""
    if recreate:
        params['recreate'] = ""
    if createonly:
        params['createonly'] = ""
    if watch in ["watch", "unwatch", "preferences", "nochange"]:
        params['watchlist'] = watch
    elif watch:
        pywikibot.warning(
            u"editpage: Invalid watch value '%(watch)s' ignored."
              % locals())
## FIXME: API gives 'badmd5' error
##        md5hash = md5()
##        md5hash.update(urllib.quote_plus(text.encode(self.encoding())))
##        params['md5'] = md5hash.digest()
    req = api.Request(site=self, **params)
    while True:
        try:
            result = req.submit()
            pywikibot.debug(u"editpage response: %s" % result,
                            _logger)
        except api.APIError, err:
            self.unlock_page(page)
            if err.code.endswith("anon") and self.logged_in():
                pywikibot.debug(
u"editpage: received '%s' even though bot is logged in" % err.code,
                                _logger)
            errdata = {
                'site': self,
                'title': page.title(withSection=False),
                'user': self.user(),
                'info': err.info
            }
            if err.code == "badtoken":
                req["token"] = self.getToken("edit", force=True)
            if err.code == "spamdetected":
                raise SpamfilterError(self._ep_errors[err.code] % errdata
                        + err.info[ err.info.index("fragment: ") + 9: ])

            if err.code == "editconflict":
                raise EditConflict(self._ep_errors[err.code] % errdata)
            if err.code in ("protectedpage", "cascadeprotected"):
                raise LockedPage(errdata['title'])
            if err.code in self._ep_errors:
                raise Error(self._ep_errors[err.code] % errdata)
            pywikibot.debug(
                u"editpage: Unexpected error code '%s' received."
                    % err.code,
                _logger)
            raise
        assert ("edit" in result and "result" in result["edit"]), result
        if result["edit"]["result"] == "Success":
            self.unlock_page(page)
            if "nochange" in result["edit"]:
                # null edit, page not changed
                pywikibot.log(u"Page [[%s]] saved without any changes."
                                % page.title())
                return True
            page._revid = result["edit"]["newrevid"]
            # see http://www.mediawiki.org/wiki/API:Wikimania_2006_API_discussion#Notes
            # not safe to assume that saved text is the same as sent
            self.loadrevisions(page, getText=True)
            return True
        elif result["edit"]["result"] == "Failure":
            if "captcha" in result["edit"]:
                captcha = result["edit"]["captcha"]
                req['captchaid'] = captcha['id']
                if captcha["type"] == "math":
                    req['captchaword'] = input(captcha["question"])
                    continue
                elif "url" in captcha:
                    webbrowser.open(captcha["url"])
                    req['captchaword'] = cap_answerwikipedia.input(
"Please view CAPTCHA in your browser, then type answer here:")
                    continue
                else:
                    self.unlock_page(page)
                    pywikibot.error(
                u"editpage: unknown CAPTCHA response %s, page not saved"
                                      % captcha)
                    return False
            else:
                self.unlock_page(page)
                pywikibot.error(u"editpage: unknown failure reason %s"
                                  % str(result))
                return False
        else:
            self.unlock_page(page)
            pywikibot.error(
u"editpage: Unknown result code '%s' received; page not saved"
                               % result["edit"]["result"])
            pywikibot.log(str(result))
            return False

APISite.editpage = _editpage

#=======================================================================

def _getToken(self, tokentype, force=False):
    """Return token retrieved from wiki to allow changing page content.

    @param tokentype: the type of token (e.g., "edit", "move", "delete");
        see API documentation for full list of types
    @param force: force to get new token
    @type force bool

    """
    if (not force) and (tokentype in self._token) and (
                  (ltime.dt.today() - self._token[tokentype][1]).seconds <
                   2 * 60 * 60):
        return self._token[tokentype][0]

    query = api.PropertyGenerator("info",
                                  titles="!",
                                  intoken=tokentype,
                                  site=self)
    for item in query:
        self._token[tokentype] = (item[tokentype + "token"], ltime.dt.today())
        return self._token[tokentype][0]

APISite.getToken = _getToken

#=======================================================================

def ___init__(self, code, fam=None, user=None, sysop=None):
    BaseSite.__init__(self, code, fam, user, sysop)
    self._namespaces = {
        # These are the MediaWiki built-in names, which always work.
        # Localized names are loaded later upon accessing the wiki.
        # Namespace prefixes are always case-insensitive, but the
        # canonical forms are capitalized
        -2: [u"Media"],
        -1: [u"Special"],
         0: [u""],
         1: [u"Talk"],
         2: [u"User"],
         3: [u"User talk"],
         4: [u"Project"],
         5: [u"Project talk"],
         6: [u"Image"],
         7: [u"Image talk"],
         8: [u"MediaWiki"],
         9: [u"MediaWiki talk"],
        10: [u"Template"],
        11: [u"Template talk"],
        12: [u"Help"],
        13: [u"Help talk"],
        14: [u"Category"],
        15: [u"Category talk"],
        }
    if self.family.versionnumber(self.code) >= 14:
        self._namespaces[6] = [u"File"]
        self._namespaces[7] = [u"File talk"]
    self.sitelock = threading.Lock()
    self._msgcache = {}
    self._loginstatus = LoginStatus.NOT_ATTEMPTED
    self._token = {}
    return

APISite.__init__ = ___init__

#=======================================================================
'''

########################################################################
########################################################################
########################################################################

#=======================================================================
# Support for finding whether the page is a redirect page from text
#=======================================================================

def _getRedirectText(self, text):
    """
    Return target of redirection. Since we obtain data from text,
    there's no need to worry about passing section.
    """
    if "site_APISite_redir" in lre.pats:
        m = lre.pats["site_APISite_redir"].match(text)
        if m:
            return m.group(1)
        else:
            return False
    else:
        lre.pats["site_APISite_redir"] = self.redirectRegex()
        return self.getRedirectText(text)

APISite.getRedirectText = _getRedirectText

#=======================================================================
# Support for finding whether pages exist
#=======================================================================

def _pagesexist(self, pages):
    def local(arr):
        text = self.parse("\n".join(
               ["* {{PAGESIZE:%s|R}}" % page.title() for page in arr]))

        for i, ps in enumerate(lre.pats["site_APISite_li"].findall(text)):
            #print arr[i], ps
            arr[i] = (arr[i], int(ps) != 0)

        return arr

    out = []
    pywikibot.output("checking pages: %d pages" % len(pages))
    while pages:
        out += local(pages[-500:])[::-1]
        del pages[-500:]
    pywikibot.output("complete!")
    return out[::-1]

APISite.pagesexist = _pagesexist

#=======================================================================
# Support for parsing text
#=======================================================================

def _parse(self, text):
    r = api.Request(site=self,
                    action="parse",
                    text=text)
    try:
        result = r.submit()
    except:
        wp.error()
    else:
        return result['parse']['text']['*']

APISite.parse = _parse

#=======================================================================
# Support for finding links in text
#=======================================================================

def _pagelinks_by_text(self, text, title=None, expand=False):
    """
    This function extract lins.
    """
    if not expand:
        links = []
        for link in lre.pats["link"].finditer(text):
            links.append("[[" + link.group("title") + "]]")
        text = "".join(links)

    r = api.Request(site=self,
                    action="parse",
                    text=text,
                    prop="links")

    if title:
        r["title"] = title

    try:
        pages = [wp.Page(item['*'])
                for item in r.submit()['parse']['links']]
    except:
        wp.error()
        return []
    else:
        return pages

APISite.pagelinks_by_text = _pagelinks_by_text

#=======================================================================
# recentchanges with repeat option
#=======================================================================

def _recentchanges(self, start=None, end=None, reverse=False,
                  namespaces=None, pagelist=None, changetype=None,
                  showMinor=None, showBot=None, showAnon=None,
                  showRedirects=None, showPatrolled=None, topOnly=False,
                  step=None, total=None, repeat=False):
    """Iterate recent changes.

    @param start: Timestamp to start listing from
    @param end: Timestamp to end listing at
    @param reverse: if True, start with oldest changes (default: newest)
    @param pagelist: iterate changes to pages in this list only
    @param pagelist: list of Pages
    @param changetype: only iterate changes of this type ("edit" for
        edits to existing pages, "new" for new pages, "log" for log
        entries)
    @param showMinor: if True, only list minor edits; if False (and not
        None), only list non-minor edits
    @param showBot: if True, only list bot edits; if False (and not
        None), only list non-bot edits
    @param showAnon: if True, only list anon edits; if False (and not
        None), only list non-anon edits
    @param showRedirects: if True, only list edits to redirect pages; if
        False (and not None), only list edits to non-redirect pages
    @param showPatrolled: if True, only list patrolled edits; if False
        (and not None), only list non-patrolled edits
    @param topOnly: if True, only list changes that are the latest revision
        (default False)

    """
    if repeat:
        reverse = True
        start = start or self.getcurrenttime()

    seen = set()
    while True:
        pywikibot.output("getting revisions...")
        if start and end:
            if reverse:
                if end < start:
                    raise Error(
            "recentchanges: end must be later than start with reverse=True")
            else:
                if start < end:
                    raise Error(
            "recentchanges: start must be later than end with reverse=False")
        rcgen = self._generator(api.ListGenerator, type_arg="recentchanges",
                                rcprop="user|comment|timestamp|title|ids"
                                       "|sizes|redirect|loginfo"
                                       #"|sizes|redirect|patrolled|loginfo" - patrol rights needed
                                       "|flags",
                                namespaces=namespaces, step=step,
                                total=total)
        if start is not None:
            rcgen.request["rcstart"] = str(start)
        if end is not None:
            rcgen.request["rcend"] = str(end)
        if reverse:
            rcgen.request["rcdir"] = "newer"
        if pagelist:
            if self.versionnumber() > 14:
                pywikibot.warning(
                    u"recentchanges: pagelist option is disabled; ignoring.")
            else:
                rcgen.request["rctitles"] = u"|".join(p.title(withSection=False)
                                                      for p in pagelist)
        if changetype:
            rcgen.request["rctype"] = changetype
        if topOnly:
            rcgen.request["rctoponly"] = ""
        filters = {'minor': showMinor,
                   'bot': showBot,
                   'anon': showAnon,
                   'redirect': showRedirects,}
                   #'patrolled': showPatrolled}
        rcshow = []
        for item in filters:
            if filters[item] is not None:
                rcshow.append(filters[item] and item or ("!"+item))
        if rcshow:
            rcgen.request["rcshow"] = "|".join(rcshow)

        for ipage in rcgen:
            if ipage['revid'] not in seen:
                seen.add(ipage['revid'])
                yield ipage

        if not repeat:
            break

        ltime.sleep(60)
        start = self.getcurrenttime() - ltime.td(seconds=72)

APISite.recentchanges = _recentchanges

########################################################################
########################################################################
########################################################################

def glob():
    lre.pats["site_APISite_li"] = lre.lre("(?<=<li>).*?(?=</li>)")

glob()
