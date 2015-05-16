''' abcnyheter.no

Supports OpenGraph (but xmlns:og is missing).

Supports schema.org:
- http://schema.org/NewsArticle
- http://schema.org/Thing
- http://schema.org/ImageObject
- http://schema.org/Person  (Author)

Meta:   title, description, image, type, url, site_name

Some interesting itemprops:
  1  datePublished
  1  articleBody
  1  author
  1  articleSection
  1  headline
  6  image      ?? is the first image the correct one?
  1  keywords
  1  text       ?? what is this for?

# Other usefull elements:
<link rel="canonical" href="..." />
<meta name="keywords"      content="comma separated keyword list" />
<meta name="news_keywords" content="comma separated keyword list" />
<meta name="revisit-after" content="1 day" />
'''

from . import OpenGraphParser

class Parser (OpenGraphParser):
    pass
