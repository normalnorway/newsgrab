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

from . import OpenGraphParser
# from opengraph import OpenGraphParser # OGParser?


class Parser (OpenGraphParser):
    def parse (self):
        meta = super(Parser,self).parse()
        meta['date'] = self.date()
        return meta
