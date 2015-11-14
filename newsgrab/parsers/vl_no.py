""" vl.no -- Vaart land. En forlengelse av KrFs kommunikasjonsavdeling? """

from . import OpenGraphParser

class Parser (OpenGraphParser):

    def parse_date (self):
        L = self.body.xpath ('//div[starts-with(@class,"byline")]//time')
        node = L.pop()
        assert not L
        # Publisert 13. november 2015
        s = ''.join (node.xpath ('text()')).strip()
        assert s.startswith ('Publisert ')
        datestr = s[10:]    # strip prefix
        #datestr = ' '.join (s.split()[1:])     # strip first word

        return self.parse_date_no (datestr)
