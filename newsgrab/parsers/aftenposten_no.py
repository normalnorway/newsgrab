''' Aftenposten.no

<time class="date published"
      itemprop="datePublished"
      datetime="2014-07-27T08:59:22Z">27.jul. 2014 10:59</time>

<time class="published"
      pubdate="pubdate"
      datetime="2015-05-31T\n21:58+01:00"</time>

Notes:
* NO-BREAK SPACE (0xA0) is used.
* some titles is prefixed with author name. e.g. "| Nils August Andresen"

@todo remove query part of image url?
image = http://www.aftenposten.no/incoming/article7605814.ece/ALTERNATES/w2048c169/afp000694277.jpg?updated=160620141138
'''

from . import OpenGraphParser

class Parser (OpenGraphParser):

    title_postfix = ' - Aftenposten'

    def parse_date (self):
        L = self.body.xpath(".//time[@itemprop='datePublished']/@datetime")
        if L:
            assert len(L) in (1,2)
            if len(L) == 2: assert L[0] == L[1]
            datestr = L[0]
        else:
            # http://www.aftenposten.no/dodsfall/Nekrolog-Nils-Christie-8039532.html
            L = self.body.xpath(".//time[@class='published']/@datetime")
            datestr = L[0].replace ('\n', '')

        return self.parse_iso_date (datestr)
