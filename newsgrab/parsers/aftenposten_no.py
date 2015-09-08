''' Aftenposten.no

<time class="date published"
      itemprop="datePublished"
      datetime="2014-07-27T08:59:22Z">27.jul. 2014 10:59</time>

Note: This is not picked up be the open graph parser
<meta name="og:description" content="...">

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

from datetime import timedelta
from . import OpenGraphParser
from . import is_dst


# get_meta_by_name helper? @see get_meta_prop

class Parser (OpenGraphParser):
    def parse (self):
        meta = super(Parser,self).parse()

        if meta['title'].endswith (' - Aftenposten'):
            meta['title'] = meta['title'][0:-14]

        meta['description'] = self.head.xpath(".//meta[@name='og:description']/@content")[0]

        # INFO:newsgrab.parsers:Found multiple datePublished; do not know howto handle

        L = self.body.xpath(".//time[@itemprop='datePublished']/@datetime")
        assert len(L) == 2
        assert L[0] == L[1]
        datestr = L[0]
        assert datestr[-1] == 'Z'

        dt = self.parse_iso_date (datestr)
        meta['date'] = dt + timedelta (hours = 2 if is_dst(dt) else 1)
        # Note: datePublised is in zulu time; must convert to local time.

        return meta
