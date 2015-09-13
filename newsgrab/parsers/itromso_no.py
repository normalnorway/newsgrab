""" itromso.no

Note: Looks like using the same publishing system as adressa.no

Output of probe.py:

Meta    image, locale, type, title, url, site_name

COUNT   ITEMPROP

Date         : Missing!
Description  : Missing!
"""

from . import OpenGraphParser

class Parser (OpenGraphParser):

    def parse (self):
        meta = super(Parser,self).parse (parse_date=False)
        meta['description'] = self.get_meta_name ('description')

        # Note: Same time zone bug as adressa.no ?
        datestr = self.get_meta_property ('article:published_time')
        meta['date'] = self.parse_iso_date (datestr)

        return meta
