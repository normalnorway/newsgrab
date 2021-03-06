""" nattogdag.no

<meta property="article:published_time" content="2015-09-15T18:15:27+00:00" />
<meta property="article:modified_time" content="2015-09-15T18:58:18+00:00" />

Output of probe.py:

Meta    locale, type, title, description, site_name, updated_time, image

COUNT   ITEMPROP
  1     articleBody
  1     datePublished
  1     headline
  1     image

Url          : Missing!   
"""

from . import OpenGraphParser

class Parser (OpenGraphParser):
    title_postfix = ' - NATT&DAG'

    def parse (self):
        meta = super(Parser,self).parse()
        meta['url'] = self.url  # og:url is missing
        return meta
