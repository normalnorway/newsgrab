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


def get_meta_prop (node, prop_name):
    L = node.xpath (".//meta[@property='%s']/@content" % prop_name)
    if len(L) == 0: return None
    if len(L) == 1: return L[0]
    raise Exception ('found multiple <meta name="%s" ... /> elements' % prop_name)


class Parser (OpenGraphParser):

    def parse (self):
        meta = super(Parser,self).parse()
        datestr = get_meta_prop (self.tree[0], 'article:published_time')
        datestr += 'Z'  # hack since parse_iso_date don't handle
        meta['date'] = self.parse_iso_date (datestr)
        return meta
