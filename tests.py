"""
Simple unit testing.

Run build-tests.py to populate testdata/.
But if testing with the same version as used to build the testdata,
the tests are worthless! So better to add json files to git?
"""

import unittest
import json
from driver import load_parser as get_parser_class
#from driver import ParserFactory

def _load_file (filename):
    with open(filename) as fp:
        return fp.read()

# tmp hack
def _dict_to_unicode (data):
    out = {}
    for key,val in data.iteritems():
        ukey = unicode (key, 'utf-8')
        if type(val) == str:
            uval = unicode (val, 'utf-8')
        else:   # datetime
            uval = unicode(val)
        out[ukey] = uval
    return out
# Fixme:
# - parser.get() returns str; json.load() returns unicode
# - parser.get() returns date as python datetime object
#   parser.get_json() returns as unicode string
#   Must do same transform here as in get_json()



class MyTestCase (unittest.TestCase):

    # @todo if testdata/ don't exists, run build-tests.py ?
#    def setUp (self):
#        self.factory = ParserFactory()

    def _load (self, pyid):
        base = 'testdata/' + pyid
        parser = get_parser_class (pyid)()
        parser.set_html (_load_file (base+'.html'))
        #data1 = parser.get()
        data1 = _dict_to_unicode (parser.get())
        data2 = json.loads (_load_file (base+'.json'))
        return data1, data2

    def test_aftenposten_no (self):
        self.assertEqual (*self._load ('aftenposten_no'))

    def test_abcnyheter_no (self):
        self.assertEqual (*self._load ('abcnyheter_no'))

    def test_dagsavisen_no (self):
        self.assertEqual (*self._load ('dagsavisen_no'))

    def test_forskning_no (self):
        self.assertEqual (*self._load ('forskning_no'))



if __name__ == '__main__':
    unittest.main()
