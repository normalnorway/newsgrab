""" www.p4.no
"""

from . import OpenGraphParser

class Parser (OpenGraphParser):

    def parse (self):
        meta = super(Parser,self).parse (parse_date=False)

        L = self.body.xpath ('//article[starts-with(@class,"main-content")]')
        article = L.pop()
        assert not L

        L = article.xpath ('//div[@class="article-byline"]/text()')
        s = L[0]
        assert s.startswith ('Publisert')
        datestr = ' '.join (s.split()[1:3])

        meta['date'] = self.parse_norwegian_date (datestr)

        return meta
