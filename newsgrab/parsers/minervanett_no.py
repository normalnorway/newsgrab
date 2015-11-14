""" minervanett.no """

from . import OpenGraphParser

class Parser (OpenGraphParser):

    def parse_date (self):
        L = self.body.xpath ('//span[@class="publishDate"]')
        node = L.pop()
        assert not L

        # 21. oktober, 2015
        s = ''.join (node.xpath ('text()')).strip()
        datestr = s.replace (',' ,'')

        return self.parse_date_no (datestr)
