""" klassekampen.no
"""

from . import OpenGraphParser

class Parser (OpenGraphParser):

    def parse (self):
        meta = super(Parser,self).parse()

        L = self.body.xpath ("//div[@class='main-titles']/*[1]") # first-child
        div = L.pop()
        assert not L
        datestr = div.text.split(' ', 1)[1]
        meta['date'] = self.parse_date_no (datestr)

        return meta
