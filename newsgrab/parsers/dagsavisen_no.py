""" dagsavisen.no

Supports Open Graph without using the namespace.

Only provides the published date, not the time :(

Must parse date manually, datePublished itemprop not supported.

Date example: Publisert 5. mars 2015

<article class="large" itemscope="" itemtype="http://schema.org/NewsArticle" role="article">
<link rel="canonical" href="...">
"""

from . import OpenGraphParser

class Parser (OpenGraphParser):
    title_postfix = ' - dagsavisen.no'

    def parse_date (self):
        expr = "//article[@role='article']/div[@class='byline']//div[@class='time']/span/text()"
        tmp = self.tree.xpath (expr)
        try:
            datestr = tmp[0].strip()
            assert len(tmp)==1
        except IndexError:
            tmp = self.tree.xpath ("//article[@role='article']//time/text()")
            datestr = ''.join (tmp).strip()
        datestr = datestr.split(' ', 1)[-1]     # remove first word
        return self.parse_date_no (datestr)
