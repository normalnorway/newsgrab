""" bt.no -- Bergens Tidende
"""

from . import OpenGraphParser

class Parser (OpenGraphParser):

    def parse (self):
        meta = super(Parser,self).parse()

        L = self.body.xpath ("//article/p[@itemprop='description']/text()")
        assert len(L)==1
        meta['description'] = L[0].strip()

        return meta
