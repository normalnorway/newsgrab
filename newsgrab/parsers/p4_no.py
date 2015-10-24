""" www.p4.no
"""

from lxml import etree
from . import OpenGraphParser


# 16.10.2015 10:40:05
from datetime import datetime
def parse_norwegian_date (datestr):
    return datetime.strptime (datestr, '%d.%m.%Y %H:%M:%S')


class Parser (OpenGraphParser):

    # charset gets screwed up for some reason. this hack fixes it
    def _create_etree (self, data):
        parser = etree.HTMLParser (encoding='utf-8')
        return etree.HTML (data, parser=parser)

    def parse (self):
        meta = super(Parser,self).parse (parse_date=False)

        L = self.body.xpath ('//article[starts-with(@class,"main-content")]')
        article = L.pop()
        assert not L

        L = article.xpath ('//div[@class="article-byline"]/text()')
        s = L[0]
        assert s.startswith ('Publisert')
        datestr = ' '.join (s.split()[1:3])

        meta['date'] = parse_norwegian_date (datestr)

        return meta
