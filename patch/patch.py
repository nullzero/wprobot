import init
from pywikibot.page import *

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

def _editTime(self):
    rev = self.latestRevision()
    if rev not in self._revisions:
        self.site.loadrevisions(self)
    return pywikibot.Timestamp.fromISOformat(self._revisions[rev].timestamp)

Page.editTime = _editTime
