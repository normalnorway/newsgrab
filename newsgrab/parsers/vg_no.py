""" vg.no

Output of probe.py:

Meta    title, description, url, type, image, site_name

COUNT   ITEMPROP
  1     articleBody
  1     author
  1     datePublished
  1     description
  1     name
  1     wordCount
"""

from . import OpenGraphParser

class Parser (OpenGraphParser):

    def parse_date (self):
        expr = '//span[@class="published" and @itemprop="datePublished"]/text()'
        L = self.body.xpath (expr)
        assert len(L)==1
        datestr = L[0].strip()
        return self.strptime (datestr, '%d.%m.%Y %H:%M')
