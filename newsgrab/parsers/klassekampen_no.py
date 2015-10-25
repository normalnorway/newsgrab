""" klassekampen.no
"""

from . import OpenGraphParser

class Parser (OpenGraphParser):

    # latin1 gives the correct result. don't ask me why
    # utf-8 raises: UnicodeDecodeError: 'utf8' codec can't decode
    #   byte 0xf8 in position 1: invalid start byte
    def _create_etree (self, data):
        from lxml import etree
        parser = etree.HTMLParser (encoding='latin1')
        return etree.HTML (data, parser=parser)

    def parse (self):
        meta = super(Parser,self).parse()

        L = self.body.xpath ("//div[@class='main-titles']/*[1]") # first-child
        div = L.pop()
        assert not L
        datestr = div.text.split(' ', 1)[1]
        meta['date'] = self.parse_date_no (datestr)

        return meta
