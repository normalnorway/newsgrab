''' osloby.no

<time class="date published"
      itemprop="datePublished"
      datetime="2015-08-30T11:47:20Z">...</time>
'''

from . import OpenGraphParser

class Parser (OpenGraphParser):

    def parse_date (self):
        L = self.body.xpath(".//time[@itemprop='datePublished']/@datetime")
        assert len(L) in (1,2)
        if len(L) == 2: assert L[0] == L[1]
        datestr = L[0]
        return self.parse_iso_date (datestr)
