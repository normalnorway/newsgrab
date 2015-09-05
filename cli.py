#!/usr/bin/env python

"""Just used for testing while developing"""

import sys
import textwrap
import logging

# don't work
#from .newsgrab import get_metadata

# will import globaly installed newgrab
#from newsgrab import get_metadata

# hack to prefer local newsgrab. @todo install in dev-mode instead
import os
sys.path.insert (0, os.getcwd())
from newsgrab import get_metadata


logging.basicConfig (level=logging.INFO)

try:
    url = sys.argv[1]
except IndexError:
    exit ('Usage: %s <url>' % sys.argv[0])

meta = get_metadata (url)

print
print 'DATE\t',     meta['date'] if meta.has_key('date') else '(missing)'
print 'TITLE\t',    meta['title']
print 'URL\t',      meta['url']
print 'IMAGE\t',    meta['image']
print '\nSUMMARY:'
print '\n'.join (textwrap.wrap (meta['description']))
print
