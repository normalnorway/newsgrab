""" pluss.vg.no

This site is behind a paywall.

No way to get the published time; only the date :(
"""

from datetime import datetime
from urlparse import urlsplit
from . import ParserBase

class Parser (ParserBase):

    def parse (self):
        meta = {}
        meta['url'] = self.url  # can also use meta property="al:web:url"
        meta['title'] = self.head.xpath ('title/text()')[0][:-6]
        meta['description'] = self.get_meta_name ('description')
        meta['image'] = self.get_meta_name ('thumbnail')

        # Get datePublished from the url. Kind of hacky.
        lst = map (int, urlsplit (self.url).path.split ('/')[1:4])
        meta['date'] = datetime (*lst)

        # @todo strip multiple spaces from description
        # @todo convert all strings in meta to unicode?
#        from pprint import pprint
#        pprint (meta)

        return meta
