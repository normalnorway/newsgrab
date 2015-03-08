#!/usr/bin/env python
import sys
import textwrap
from __init__ import get_metadata

try:
    url = sys.argv[1]
except IndexError:
    exit ('Usage: %s <url>' % sys.argv[0])

meta = get_metadata (url)

print
print 'DATE\t',     meta['date']
print 'TITLE\t',    meta['title']
print 'URL\t',      meta['url']
print 'IMAGE\t',    meta['image']
print '\nSUMMARY:'
print '\n'.join (textwrap.wrap (meta['description']))
print
