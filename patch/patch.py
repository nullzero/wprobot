import init
from pywikibot.page import *

def _getVersionHistory(self, reverseOrder=False, step=None,
                      total=None):
    """Load the version history page and return history information.

    Return value is a list of tuples, where each tuple represents one
    edit and is built of revision id, edit date/time, user name, and
    edit summary. Starts with the most current revision, unless
    reverseOrder is True.

    @param step: limit each API call to this number of revisions
    @param total: iterate no more than this number of revisions in total

    """
    self.site.loadrevisions(self, getText=False, rvdir=reverseOrder,
                              step=step, total=total)
    return [ ( self._revisions[rev].revid,
               pywikibot.Timestamp.fromISOformat(self._revisions[rev].timestamp),
               self._revisions[rev].user,
               self._revisions[rev].comment
             ) for rev in sorted(self._revisions,
                                 reverse=not reverseOrder)
           ]

Page.getVersionHistory = _getVersionHistory

def _fullVersionHistory(self, reverseOrder=False, step=None,
                      total=None):
    """Iterate previous versions including wikitext.

    Takes same arguments as getVersionHistory.

    @return: A generator that yields tuples consisting of revision ID,
        edit date/time, user name and content

    """
    self.site.loadrevisions(self, getText=True,
                            rvdir=reverseOrder,
                            step=step, total=total)
    return [( self._revisions[rev].revid,
              pywikibot.Timestamp.fromISOformat(self._revisions[rev].timestamp),
              self._revisions[rev].user,
              self._revisions[rev].text
            ) for rev in sorted(self._revisions,
                                reverse=not reverseOrder)
           ]

Page.fullVersionHistory = _fullVersionHistory
