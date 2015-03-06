''' abcnyheter.no

Supports OpenGraph (but xmlns:og is missing).

Supports schema.org:
- http://schema.org/NewsArticle
- http://schema.org/Thing
- http://schema.org/ImageObject
- http://schema.org/Person  (Author)

# Other usefull elements:
<link rel="canonical" href="..." />
<meta name="keywords"      content="comma separated keyword list" />
<meta name="news_keywords" content="comma separated keyword list" />
<meta name="revisit-after" content="1 day" />
'''

from . import OpenGraphParser

class Parser (OpenGraphParser):
    def parse (self):
        meta = super(Parser,self).parse()
        meta['date'] = self.parse_date()
        return meta
