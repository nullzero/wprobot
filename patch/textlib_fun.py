import pywikibot.textlib

def _getLanguageLinks(text, insite=None, pageLink="[[]]",
                     template_subpage=False):
    """
    Return a dict of interlanguage links found in text.

    Dict uses language codes as keys and Page objects as values.
    Do not call this routine directly, use Page.interwiki() method
    instead.

    """
    if insite is None:
        insite = pywikibot.getSite()
    fam = insite.family
    # when interwiki links forward to another family, retrieve pages & other
    # infos there
    if fam.interwiki_forward:
        fam = pywikibot.Family(fam.interwiki_forward)
    result = {}
    # Ignore interwiki links within nowiki tags, includeonly tags, pre tags,
    # and HTML comments
    tags = ['comments', 'nowiki', 'pre', 'source']
    if not template_subpage:
        tags += ['includeonly']
    text = removeDisabledParts(text, tags)

    # This regular expression will find every link that is possibly an
    # interwiki link.
    # NOTE: language codes are case-insensitive and only consist of basic latin
    # letters and hyphens.
    # TODO: currently, we do not have any, but BCP 47 allows digits, and
    #       underscores.
    # TODO: There is no semantic difference between hyphens and
    #       underscores -> fold them.
    interwikiR = re.compile(r'\[\[([a-zA-Z\-]+)\s?:([^\[\]\n]*)\]\]')
    for lang, pagetitle in interwikiR.findall(text):
        lang = lang.lower()
        # Check if it really is in fact an interwiki link to a known
        # language, or if it's e.g. a category tag or an internal link
        if lang in fam.obsolete:
            lang = fam.obsolete[lang]
        if lang in fam.langs.keys():
            if '|' in pagetitle:
                # ignore text after the pipe
                pagetitle = pagetitle[:pagetitle.index('|')]
            # we want the actual page objects rather than the titles
            site = pywikibot.getSite(code=lang, fam=fam)
            try:
                result[site] = pywikibot.Page(site, pagetitle)
            except pywikibot.InvalidTitle:
                pywikibot.output(u'[getLanguageLinks] Text contains invalid '
                                 u'interwiki link [[%s:%s]].'
                                 % (lang, pagetitle))
                continue
    return result

pywikibot.textlib.getLanguageLinks = _getLanguageLinks # Use inside textlib.py
pywikibot.getLanguageLinks = _getLanguageLinks # Use outside textlib.py
