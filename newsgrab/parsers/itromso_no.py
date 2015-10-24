""" itromso.no

Looks like using the same publishing system as adressa.no
Same time zone bug as adressa.no?
"""

from . import OpenGraphParser

class Parser (OpenGraphParser):

    def parse (self):
        meta = super(Parser,self).parse()
        meta['description'] = self.get_meta_name ('description')
        return meta
