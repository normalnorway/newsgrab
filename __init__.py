#from urlparse import urlparse
from driver import ParserFactory
from driver import domain_to_pyid   # @todo move to this file?


_factory = ParserFactory()


# This is the public API. It will keep an internal cache of the parsers.
def get_metadata (url):
    parser = _factory.get (url)
    return parser.get()


def get_metadata_as_json (url):
    parser = _factory.get (url)
    return parser.get_as_json()


#import json
#meta['date'] = str (meta['date'])
#json.dump (meta, sys.stdout)
#print


#domain = sys.argv[1]
#parser = factory.get ('http://' + domain)
#parser.set_html (open ('testdata/%s.html' % domain_to_pyid(domain)).read())
#meta = parser.get()
