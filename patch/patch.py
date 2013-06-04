import init
from pywikibot.page import *

def _editTime(self):
    rev = self.latestRevision()
    if rev not in self._revisions:
        self.site.loadrevisions(self)
    return pywikibot.Timestamp.fromISOformat(self._revisions[rev].timestamp)

Page.editTime = _editTime
