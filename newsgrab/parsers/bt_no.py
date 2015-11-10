""" bt.no -- Bergens Tidende

Some articles uses this date format:
<time class="published"
      pubdate="pubdate"
      datetime="2015-10-17 22:00:22 CEST">...</time>

"""

from . import OpenGraphParser

class Parser (OpenGraphParser):

    def parse (self):
        meta = super(Parser,self).parse()
        if 'date' in meta:
            return meta

        # http://www.bt.no/nyheter/lokalt/Vanskelig-a-avslore-Judas-drap-3461791.html
        # Note: These are behind a paywall
        L = self.body.xpath ('//time[@class="published"]/@datetime')
        assert len(L) == 1
        date, time, tz = L[0].split()   # '2015-10-17 22:00:22 CEST'
        assert tz in ('CET', 'CEST')
        datestr = date + 'T' + time
        meta['date'] = self.parse_iso_date (datestr)

        #meta['paywall'] = True
        return meta

        # Note: Might include html in the description. Or is that just a bug?
        # http://www.bt.no/share/article-3086840.html
        # Wierd way to clean all html tags
#        from lxml import etree
#        div = etree.fromstring ('<div>%s</div>' % meta['description'])
#        meta['description'] = ''.join (div.xpath('//*/text()'))
