"""
@todo fix this
INFO:newsgrab.parsers:Found multiple datePublished; do not know howto handle

<article class     = "article widget rich surrogate-content container-widget cf"
         role      = "main"
         data-id   = "1.11585406"
         itemscope = ""
         itemtype  = "http://schema.org/Article">
"""

from . import OpenGraphParser

class Parser (OpenGraphParser):

    def parse (self):
        meta = super(Parser,self).parse()

        L = self.tree.xpath("//article[@role='main']")
        article = L.pop()
        assert L == []

        L = article.xpath("//time[@itemprop='datePublished']/@datetime")
        assert len(L) == 2  # found both on start and end of article
        datestr = L[0]

        meta['date'] = self.parse_iso_date (datestr)
        return meta
