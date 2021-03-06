"""
Can use as command line interface:
$ python -m newsgrab <url>
"""

# XXX Put code inside main()

import sys
import textwrap
import logging
from newsgrab import get_metadata

logging.basicConfig (level=logging.INFO)

try:
    url = sys.argv[1]
except IndexError:
    exit ('Usage: python -m newsgrab <url>')

meta = get_metadata (url)

print
print 'DATE\t',     meta['date'] if 'date' in meta else '(missing)'
print 'TITLE\t',    meta['title']
print 'URL\t',      meta['url']
print 'IMAGE\t',    meta['image'] if 'image' in meta else '(missing)'
print '\nSUMMARY:'
if 'description' in meta:
    print '\n'.join (textwrap.wrap (meta['description']))
else:
    print '(missing)'
print
