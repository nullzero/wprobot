import init
from pywikibot import *

def _totimestampformat(self):
    return self.strftime(self.mediawikiTSFormat)

pywikibot.Timestamp.totimestampformat = _totimestampformat
