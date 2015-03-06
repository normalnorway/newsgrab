#!/usr/bin/env python
"""
Probes an url (news article) for OpenGraph metadata support.
"""

import os, sys
import urllib2
from lxml import etree

try:
    fp = open (sys.argv[1])
except IOError:
    fp = urllib2.urlopen (sys.argv[1])

tree = etree.HTML (fp.read())
xpath = tree.xpath

def itemprop (key):
    elems = xpath ("//*[@itemprop='%s']/text()" % key)
    if not elems: return None
    if len(elems) > 1: print 'itemprop: multiple elements matches'
    return elems[0].strip()

def flatten (lst):
    return sum (lst, [])


has_meta = set()

#print 'datePublished\t', itemprop ('datePublished')

# @todo check for /html/body/meta?
# @todo og:type == article


## 1. Check for header meta tags
L = xpath ('/html/head/meta[starts-with(@property,"og:")]')
if not L: L = []
#print 'Meta\t', ', '.join (e.get('property') for e in L)
print 'Meta\t', ', '.join (e.get('property')[3:] for e in L)
has_meta.update (e.get('property')[3:] for e in L)
##print 'Meta\t', [e.get('property') for e in L]


## 2. Check for itemprop=datePublished
if itemprop ('datePublished'):
    has_meta.add ('date')


#from collections import Counter
#cnt = Counter(e.attrib['itemtype'] for e in xpath("//*[@itemtype]"))
#for key,val in cnt.items():
#    print '%3d\t%s' % (int(val), key)
#exit(0)


# @todo must split attrib on whitespace
from collections import Counter
#cnt = Counter(e.attrib['itemprop'] for e in xpath("//*[@itemprop]"))
#for key,val in cnt.items():
#    print '%3d\t%s' % (int(val), key)

cnt = Counter()
for e in xpath("//*[@itemprop]"):
    cnt.update (e.attrib['itemprop'].split())
#print '\nCount   Itemprop\n======================='
print '\nCOUNT   ITEMPROP'
for key,val in sorted (cnt.items()):
    print '%3d\t%s' % (int(val), key)


#from collections import Counter
#cnt = Counter(e.attrib['itemprop'] for e in xpath("//*[@itemprop]"))
#meta = dict (cnt.items())
#print meta
#exit(0)
#assert meta['date']
#assert meta['title']
#assert meta['url']
#assert meta['image']
#assert meta['description']

print
for feature in ('date', 'title', 'description', 'image', 'url'):
    if not feature in has_meta:
        print '%-12s : Missing!' % feature.title()
