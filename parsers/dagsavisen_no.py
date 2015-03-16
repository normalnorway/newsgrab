''' abcnyheter.no

Supports Open Graph without using the namespace.

Only provides the published date, not the time :(
Must parse date manually, datePublished itemprop not supported

Note: Uses Norwegian month names, so need date parser that handles this.

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
        #return datetime.strptime (datestr, 'Publisert %d. %B %Y')
        # XXX: tmp hack
        import locale
        oldloc = locale.getlocale()
        locale.setlocale(locale.LC_TIME, "nb_NO.UTF-8")
        date = datetime.strptime (datestr, 'Publisert %d. %B %Y')
        locale.setlocale(locale.LC_TIME, '.'.join(oldloc) if oldloc[0] else "C")
        return date

    def parse (self):
        meta = super(Parser,self).parse()
        meta['date'] = self.parse_date()
        if meta['title'].endswith ('- dagsavisen.no'):
            meta['title'] = meta['title'][:-16] # remove branding
        return meta
