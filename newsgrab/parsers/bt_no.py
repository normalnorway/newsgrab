""" bt.no -- Bergens Tidende

Some articles uses this date format:
UPDATE: Looks like all artices uses this format
<time class="published"
      pubdate="pubdate"
      datetime="2015-10-17 22:00:22 CEST">...</time>

"""

from . import OpenGraphParser

class Parser (OpenGraphParser):
    pass
