"""
Simple unit testing.

Run build-tests.py to populate testdata/.
But if testing with the same version as used to build the testdata,
the tests are worthless! So better to add json files to git?
"""

import unittest
import json
from driver import load_parser as get_parser_class


def _load_file (filename):
    with open(filename) as fp:
        return fp.read()


class MyTestCase (unittest.TestCase):

    def _load (self, pyid):
        base = 'testdata/' + pyid
        parser = get_parser_class (pyid)()
        parser.set_html (_load_file (base+'.html'))
        data1 = parser.get()
        data1[u'date'] = unicode(data1['date']) # hack: datetime -> unicode
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

    def test_vg_no (self):
        self.assertEqual (*self._load ('vg_no'))



if __name__ == '__main__':
    unittest.main()
