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
    _video = False

    # http://www.nrk.no/video/PS*191550
    def handle_nrk_video (self, meta):
        self._video = True
        meta['url'] = self.url
        # XXX no way to get the date. it's populated with javascript :(
        return meta


    def parse_date (self):
        if self._video: return None

        L = self.body.xpath ("//article[@role='main']")
        if len(L) == 0:
            # http://www.nrk.no/nyheter/1.12667345
            L = self.body.xpath (".//time[@class='relative bulletin-time']/@datetime")
            return self.parse_iso_date (L[0])

        article = L.pop()
        assert L == []

        L = article.xpath (".//time[@itemprop='datePublished']/@datetime")
        if len(L) == 0: # some articles uses this format (/urix/xl/)
            L = article.xpath (".//time[@class='relative']/@datetime")
            assert len(L)==1
            return self.parse_iso_date (L[0])

        assert len(L) == 2  # found both on start and end of article
        datestr = L[0]

        return self.parse_iso_date (datestr)


    def parse (self):
        meta = super(Parser,self).parse()

        # Handle nrk.no/video/
        from urlparse import urlsplit
        obj = urlsplit (self.url)
        if obj.path.startswith ('/video/'):
            return self.handle_nrk_video (meta)

        return meta
