# encoding: utf-8
''' abcnyheter.no

Supports OpenGraph (but without xmlns:og).

Supports schema.org:
- http://schema.org/NewsArticle
- http://schema.org/Thing
- http://schema.org/ImageObject
- http://schema.org/Person  (Author)

# Other usefull elements:
<link rel="canonical" href="http://www.abcnyheter.no/nyheter/2014/02/28/brukte-pressen-til-lokke-narko-siktet-politiker-i-felle" />
<meta name="keywords"      content="Bergen,Eirik Jensen,erik skutle,hasj,Høyre,John Christian Elden,narkotika,politiet,Norge,nyheter" />
<meta name="news_keywords" content="Bergen,Eirik Jensen,erik skutle,hasj,Høyre,John Christian Elden,narkotika,politiet,Norge,nyheter" />
<meta name="revisit-after" content="1 day" />
'''

from datetime import datetime
from . import OpenGraphParser


# @todo move to init.
# @todo and make more general (should be part of schema.org parser)
def get_itemprop (elem, key):   # elem=span
    return elem.xpath ("//span[@itemprop='%s']/text()" % key)[0].strip()


class Parser (OpenGraphParser):
    def parse (self):
        meta = self.parse_opengraph()

        # p.byline-date > span.itemprop=datePublished
        #tmp = content.xpath ("//span[@itemprop='datePublished']/text()")[0]
        #tmp = content.xpath ("//span[@itemprop='datePublished']")[0].text.strip()
        datestr = get_itemprop (self.tree, 'datePublished')
        meta['date'] = datetime.strptime (datestr, '%Y-%m-%dT%H:%M:%S')
        # %T is equivalent to %H:%M:%S
        # ... but not supported in Python :(

        return meta
