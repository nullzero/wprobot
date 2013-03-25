from wp import lre

class Redirect(object):
    def __init__(self, site):
        self.site = site
        self.regex = None
    
    def redirectRegex(self):
        """Return a compiled regular expression matching on redirect pages.

        Group 1 in the regex match object will be the target title.

        """
        if self.regex:
            return self.regex
            
        #NOTE: this is needed, since the API can give false positives!
        default = 'REDIRECT'
        keywords = self.site.versionnumber() > 13 and self.site.getmagicwords('redirect')
        if keywords:
            pattern = r'(?:' + '|'.join(keywords) + ')'
        else:
            # no localized keyword for redirects
            pattern = r'#%s' % default
        if self.site.versionnumber() > 12:
            # in MW 1.13 (at least) a redirect directive can follow whitespace
            prefix = r'\s*'
        else:
            prefix = r'[\r\n]*'
        # A redirect starts with hash (#), followed by a keyword, then
        # arbitrary stuff, then a wikilink. The wikilink may contain
        # a label, although this is not useful.
        self.regex = lre.lre(u"(?ius)" + prefix + pattern
                                 + '\s*:?\s*\[\[(.+?)(?:\|.*?)?\]\]')
        return self.regex
    
    
