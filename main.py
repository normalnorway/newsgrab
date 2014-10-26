import sys
from __init__ import get_metadata

url = sys.argv[1]
meta = get_metadata (url)

print
print 'DATE\t',     meta['date']
print 'TITLE\t',    meta['title']
print 'URL\t',      meta['url']
print 'IMAGE\t',    meta['image']
print 'SUMMARY\n',  meta['summary']
print
