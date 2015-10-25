""" tv2.no - norges daarligste nyhetskanal
"""

from . import OpenGraphParser

class Parser (OpenGraphParser):
    strip_title = ' - TV2.no'

    def parse (self):
        meta = super(Parser,self).parse()

        datestr = self.get_meta_property ('rnews:datePublished')
        meta['date'] = self.strptime (datestr, '%Y/%m/%d %H:%M:%S')

        return meta
