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
    # This db article uses differente date parsing code. @todo test both
    #'http://www.dagbladet.no/2015/01/16/kultur/meninger/debatt/37198268/',
    'http://www.nrk.no/ytring/to-historier-om-ruspolitikk-1.11585406',
    'http://www.ba.no/apen-om-eget-rusmisbruk/s/5-8-146941',
    'http://www.nordlys.no/hasj/narkotika/sosiale-medier/jeg-skulle-onske-at-flere-tok-avstand-fra-dette/s/5-34-237040',
    'http://www.osloby.no/nyheter/krim/Lagret-90-kilo-hasj-og-5_9-kilo-kokain-i-leilighet-pa-Romsas-8142565.html',
    'http://nettavisen.no/artikkel/8487912',
    'http://www.adressa.no/nyheter/politikk/valget/article11546150.ece',
    'http://www.itromso.no/nyheter/article10796258.ece',
    'http://www.nattogdag.no/2015/09/portugals-ruspolitikk-er-ikke-perfekt-men-den-funker/',
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


#create_testdata()
#exit(0)


import unittest
import json

class MyTestCase (unittest.TestCase):
    maxDiff = None
    def load_data (self, url):
        """Parse url into json and load json from testdata (returns both)"""
        data1 = json.load (open(filename_from_url (url)))
        data2 = get_parser (url).get()
        data2[u'date'] = unicode (data2['date']) # datetime -> unicode
        return data1, data2     # data_parsed, data_fixture


# Add tests to MyTestCase
for url in urls_to_test:
    name = 'test_' + id_from_url (url)
    setattr (MyTestCase, name, lambda self,url=url: # url=url: lambda capture
                self.assertEqual (*self.load_data (url)))



if __name__ == '__main__':
    import sys
    if not (len(sys.argv)>1 and sys.argv[1]=='fixture'):
        unittest.main()
        exit(0)
    create_testdata()
    # @todo possible to update fixtures (overwrite)
    # @todo possible to only create/update one fixture
