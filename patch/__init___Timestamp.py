# -*- coding: utf-8  -*-

import init
from pywikibot import *

#=======================================================================
# Support for extracting timestamp format
#=======================================================================

def _totimestampformat(self):
    return self.strftime(self.mediawikiTSFormat)

Timestamp.totimestampformat = _totimestampformat
