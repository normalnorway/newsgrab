""" Bergensavisen - www.ba.no

Date is found both in header and in the body:

/html/head
<meta property="article:published_time" content="2015-09-03T15:29:30.000Z" />
<meta property="article:modified_time" content="2015-09-03T18:14:03.000+0200" />
Note: Time zone is not consistent :(

/html/body
<time datetime="2015-09-03T15:29:30.000Z" itemprop="datePublished">03. september 2015, kl. 17:29</time>

# Other notes:

<meta property="og:type" content="story" />
But article:published_time is still defined (even if for content=article).

Note: 'og:url' has query parameters appended. Strip or use rel=canonical.

<link rel="canonical" href="http://www.ba.no/apen-om-eget-rusmisbruk/s/5-8-146941" />
"""

from . import OpenGraphParser

# @todo improve datePublished in parse(); then can drop date handling here?

class Parser (OpenGraphParser):
    # og:url has (unwanted) query parameters appended, so don't use
    use_canonical_url = True

    def parse (self):
        meta = super(Parser,self).parse()

        datestr = self.get_meta_property ('article:published_time')
        assert datestr[-1] == 'Z'
        meta['date'] = self.parse_iso_date (datestr)

#        body = self.body
#        L = body.xpath (".//main/article[@itemtype='http://schema.org/Article']")
#        assert len(L) == 1
#        article = L.pop()

        return meta
