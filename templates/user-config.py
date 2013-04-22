# -*- coding: utf-8  -*-

"""
Example
-------
family = 'Nullzerobot'
usernames['wikipedia']['th'] = family      #  Wikipedia bot
usernames['wikibooks']['th'] = family       # Wikibooks bot
usernames['wikidata']['wikidata'] = family  # Wikidata  bot
usernames['wikidata']['repo'] = u'demo'     # Wikidata  test
usernames['i18n']['i18n'] = u'Nullzero'     # i18n      id
usernames['test']['test'] = u'Nullzero'
sysopnames['wikibooks']['th'] = u'Nullzero' # Wikibooks sysop
sysopnames['wikipedia']['th'] = u'Nullzero' # Wikipedia sysop

password_file = os.path.join(<!-- bot dir here -->, ".passwd")

family = 'wikipedia'
mylang = 'th'
"""

max_queue_size = 30
minthrottle = 0
maxthrottle = 1
put_throttle = 0
special_page_limit = 5000
