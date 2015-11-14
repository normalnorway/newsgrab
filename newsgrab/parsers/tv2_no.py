""" tv2.no -- norges daarligste nyhetskanal """

from . import OpenGraphParser

class Parser (OpenGraphParser):
    strip_title = ' - TV2.no'

    def parse_date (self):
        datestr = self.get_meta_property ('rnews:datePublished')
        return self.strptime (datestr, '%Y/%m/%d %H:%M:%S')
