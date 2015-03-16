"""
Used while developing to simplify testing.

$ python test.py <filename>
$ python test.py <url>
"""

import sys, os
from urlparse import urlsplit
from driver import domain_to_parser_id

import logging
logging.basicConfig (level=logging.DEBUG)

# Some sites requires a Norwegian locale for the date parsing
# functions to work. Dagsavisen,
#import locale
#locale.setlocale (locale.LC_TIME, 'nb_NO.utf8')


# Load file or url
try:
    filename = sys.argv[1]
    fp = open (filename)
    base,ext = os.path.splitext (os.path.basename (filename))
    parser_id = base
except IOError:
    import urllib2
    url = sys.argv[1]
    fp = urllib2.urlopen (url)
    parser_id = domain_to_parser_id (urlsplit(url).hostname)
except IndexError:
    exit ('Usage: %s <url>|<filename>' % sys.argv[0])


# Load parser
# @todo driver.load_parser_class
try:
    mod = __import__ ('parsers.'+parser_id, fromlist=['Parser'])
    parser = mod.Parser()
except ImportError as ex:
    print >>sys.stderr, "WARNING: No custom parser. Using OpenGraphParser"
    from parsers import OpenGraphParser
    parser = OpenGraphParser()

#if filename:
#    parser.set_html (fp.read())
#elif url:
#    parser.set_url (url)

print "###", parser_id
parser.set_html (fp.read())
parser.url = parser_id
data = parser.get()

#from pprint import pprint
#pprint (data)
#exit(0)

for key,val in data.iteritems():
    print '# %s\n[%s]\n' % (key.ljust(8), val)
    #print '%s <%s>' % (key.ljust(8), val)
    #print key.ljust(10), val
