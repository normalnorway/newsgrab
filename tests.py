"""
Simple test system.

Run parser on set of urls and compares to existing data.

$ python tests.py MyTestCase.test_nattogdag_no
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
    'http://www.t-a.no/nyheter/article11305842.ece',
    'http://www.bt.no/nyheter/lokalt/Narko-motstander-tatt-med-12-kilo-cannabis-3065875.html',
    'http://pluss.vg.no/2015/10/16/2179/2179_23543040',
    'http://www.p4.no/story.aspx?id=633306',
    'http://www.klassekampen.no/article/20151024/ARTICLE/151029898',
    'http://www.tv2.no/a/7522532',
    'http://tidsskriftet.no/article/1495645',
]

# These urls triggered bugs in the parsers. The bugs are fixed, but also
# tests these urls.
#http://www.dagbladet.no/2015/01/08/kultur/meninger/debatt/kronikk/cannabis/37073467/
#http://www.dagbladet.no/2015/01/06/nyheter/innenriks/utenriks/cannabis/marihuana/36978662/
#http://www.abcnyheter.no/nyheter/2015/07/15/194410653/legalisering-vil-gi-faerre-dodsfall
#http://www.aftenposten.no/fakta/innsikt/Snuser-pa-muligheten-for-a-legalisere-marihuana-7983917.html
#http://www.dagbladet.no/2014/02/06/kultur/meninger/hovedkronikk/31668467/
#http://www.dagbladet.no/2014/02/27/nyheter/samfunn/politikk/erna_solberg/hoyre/32065499/
#http://www.dagbladet.no/2015/07/15/kultur/debatt/meninger/cannabis/kronikk/40147871/
#http://www.aftenposten.no/meninger/kronikker/Kronikk-av-Willy-Pedersen-Ruspolitisk-regjeringsskifte-i-2017-7931465.html
#http://www.aftenposten.no/meninger/kronikker/Etterlyst-En-kunnskapsbasert-ruspolitikk-7971175.html
#http://www.aftenposten.no/helse/Norge-har-flest-overdosedodsfall-i-Norden-7925879.html
#http://www.abcnyheter.no/reise/2015/02/25/218756/jamaica-opphever-marihuanaforbud
#http://www.abcnyheter.no/nyheter/2014/01/20/191569/obama-marihuana-ikke-farligere-enn-alkohol
#http://www.abcnyheter.no/livet/2014/10/21/210209/cannabis-og-hasj-er-farligere-na-enn-foer
#http://www.abcnyheter.no/nyheter/2012/11/04/162048/lege-vil-starte-cannabisbehandling-i-norge
#http://www.aftenposten.no/dodsfall/Nekrolog-Nils-Christie-8039532.html


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
