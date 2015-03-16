#!/usr/bin/env python
import sys
import textwrap
import logging
from __init__ import get_metadata

logging.basicConfig (level=logging.INFO)

try:
    url = sys.argv[1]
except IndexError:
    exit ('Usage: %s <url>' % sys.argv[0])

meta = get_metadata (url)

#from pprint import pprint
#pprint (meta)
#exit(0)

print
print 'DATE\t',     meta['date']
print 'TITLE\t',    meta['title']
print 'URL\t',      meta['url']
print 'IMAGE\t',    meta['image']
print '\nSUMMARY:'
print '\n'.join (textwrap.wrap (meta['description']))
print
