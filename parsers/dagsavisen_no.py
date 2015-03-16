''' abcnyheter.no

Supports Open Graph without using the namespace.

Only provides the published date, not the time :(
Must parse date manually, datePublished itemprop not supported

NOTE: Locale must be set to recognize Norwegian month names!
@todo parser that don't rely on this?

<article class="large" itemscope="" itemtype="http://schema.org/NewsArticle" role="article">
<link rel="canonical" href="http://www.dagsavisen.no/verden/mulig-vendepunkt-i-irak-1.320192">
'''

from . import OpenGraphParser
from datetime import datetime

class Parser (OpenGraphParser):
    def parse_date (self):
        expr = "//article[@role='article']/div[@class='byline']//div[@class='time']/span/text()"
        tmp = self.tree.xpath (expr)
        assert len(tmp)==1
        datestr = tmp[0].strip()
        return datetime.strptime (datestr, 'Publisert %d. %B %Y')

    def parse (self):
        meta = super(Parser,self).parse()
#        meta['date'] = self.parse_date()
        if meta['title'].endswith ('- dagsavisen.no'):
            meta['title'] = meta['title'][:-16] # remove branding
        return meta
