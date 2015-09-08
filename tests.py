"""
Simple test system.

Run parser on set of urls and compares to existing data.
"""

# Note: Can one have one url per domain. @todo fix that
urls_to_test = [
    'http://www.aftenposten.no/nyheter/uriks/The-New-York-Times-krever-cannabislegalisering-i-hele-USA-7649727.html',
    'http://www.abcnyheter.no/nyheter/2014/02/28/brukte-pressen-til-lokke-narko-siktet-politiker-i-felle',
    'http://www.dagsavisen.no/verden/mulig-vendepunkt-i-irak-1.320192',
    'http://forskning.no/2014/10/hvor-farlig-er-cannabisbruk',
    'http://www.vg.no/forbruker/helse/helse-og-medisin/professor-om-cannabis-behandling-ingen-sikker-effekt/a/23383207/',
    'http://www.dagbladet.no/2015/01/30/kultur/kulturnytt/cannabis/narkotika/hasj/37448273/',
    'http://www.nrk.no/ytring/to-historier-om-ruspolitikk-1.11585406',
    'http://www.ba.no/apen-om-eget-rusmisbruk/s/5-8-146941',
]

import os
BASE = os.path.dirname (__file__)
DATADIR = os.path.join (BASE, 'fixture')

# @todo better if can call get_parser_class on url, then don't need to
# mess with domain_to_pyid? UPDATE: pyid is also need for json filename

def id_from_url (url):
    from urlparse import urlsplit
    from newsgrab.driver import domain_to_pyid
    urlobj = urlsplit (url)
    return domain_to_pyid (urlobj.hostname)

def get_parser (url):    # get_parser_by_url, get_parser_for_url?
    from newsgrab.driver import load_parser as get_parser_class
    pyid = id_from_url (url)
    return get_parser_class (pyid)(url)
    #return get_parser_class (pyid)()

def filename_from_url (url):
    return os.path.join (DATADIR, id_from_url(url) + '.json')

# store_file, store_as_file, save_file
def set_file_contents (filename, contents):
    with open (filename, 'w') as fp:
        fp.write (contents)



def create_testdata (skip_existing=True):
    """Populates DATADIR by parsing all urls and save as json"""
    if not os.path.isdir (DATADIR):
        os.mkdir (DATADIR)
    for url in urls_to_test:
        filename = filename_from_url (url)
        if skip_existing and os.path.exists (filename):
            print 'Skipping', filename
            continue
        print 'Parsing into', filename
        # @todo try/except
        parser = get_parser (url)
        set_file_contents (filename, parser.get_json())



import unittest
import json

class MyTestCase (unittest.TestCase):
    def load_data (self, url):
        """Parse url into json and load json from testdata (returns both)"""
        data1 = json.load (open(filename_from_url (url)))
        data2 = get_parser (url).get()
        data2[u'date'] = unicode (data2['date']) # datetime -> unicode
        return data1, data2     # data_parsed, data_fixture


# Add tests to MyTestCase
for url in urls_to_test:
    name = 'test_' + id_from_url (url)
    setattr (MyTestCase, name, lambda self:
                self.assertEqual (*self.load_data (url)))


if __name__ == '__main__':
    unittest.main()


exit(0)


# @todo must ignore unknown args so this works: python tests.py -v
if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        print 'fixme'
    elif sys.argv[1] in ['help', '--help', '-h']:
        print 'usage: [help|init]'
    elif sys.argv[1] == 'init':
        create_testdata()
    else:
        print 'syntax error'
