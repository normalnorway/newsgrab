''' abcnyheter.no

Supported OpenGraph properties:
title, url, description, og:image, type, locality

<meta content="2014-02-28T13:58:08" property="article:published_time">

# Other usefull elements
<link href="..." rel="canonical">

<meta content="Nyheter" property="article:section">

<meta content="keyword1,keyword2,..." name="keywords">
<meta content="keyword1,keyword2,..." name="news_keywords">

<meta content="bergen" property="article:tag">
<meta content="nyheter" property="article:tag">
one element per keyword
'''

from . import OpenGraphParser


class Parser (OpenGraphParser):
    title_postfix = ' | ABC Nyheter'

    def parse (self):
        meta = super(Parser,self).parse()

        datestr = self.get_meta_property ('article:published_time')
        meta['date'] = self.parse_iso_date (datestr)
        return meta
