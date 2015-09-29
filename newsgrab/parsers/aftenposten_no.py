''' Aftenposten.no

<time class="date published"
      itemprop="datePublished"
      datetime="2014-07-27T08:59:22Z">27.jul. 2014 10:59</time>

Note: This is not picked up be the open graph parser
<meta name="og:description" content="...">

Note: NO-BREAK SPACE (0xA0) is used.

@todo remove query part of image url?
image = http://www.aftenposten.no/incoming/article7605814.ece/ALTERNATES/w2048c169/afp000694277.jpg?updated=160620141138

# Output from probe.py
Meta    site_name, title, url, image, type
itemprop: multiple elements matches

COUNT   ITEMPROP
  1     articleBody
  1     author
  1     dateModified
  2     datePublished
  1     description
  1     email
  1     headline
  2     name

Description  : Missing!
'''

from . import OpenGraphParser

# Note: some titles is prefixed with author name: | Nils August Andresen

class Parser (OpenGraphParser):

    title_postfix = ' - Aftenposten'

    def parse (self):
        meta = super(Parser,self).parse (parse_date=False)

        meta['description'] = self.get_meta_name ('og:description')

        L = self.body.xpath(".//time[@itemprop='datePublished']/@datetime")
        assert len(L) in (1,2)
        if len(L) == 2:
            assert L[0] == L[1]
        datestr = L[0]
        assert datestr[-1] == 'Z'
        meta['date'] = self.parse_iso_date (datestr)

        return meta
