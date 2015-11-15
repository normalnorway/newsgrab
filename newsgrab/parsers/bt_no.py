""" bt.no -- Bergens Tidende

Some articles uses this date format:
UPDATE: Looks like all non-paywall artices uses this format
<time class="published"
      pubdate="pubdate"
      datetime="2015-10-17 22:00:22 CEST">...</time>

Paywall:
http://www.bt.no/meninger/kommentar/Mathias_Fischer/Cannabis-i-Canada-3463151.html
"""

from . import OpenGraphParser

class Parser (OpenGraphParser):
    pass

    # Note: Only called if parse() is unable to parse the date.
    # Update: No, this will override the generic date parsing,
    # unless super() is called.
#    def parse_date (self):
#        dt = super (Parser, self).parse_date()
#        if dt: return dt
#
#        L = self.body.xpath ('//dd[@class="pubDate"]/time/@datetime')
#        if len(L) > 0:
#            assert len(L) == 1
#            # 2015-10-20 12:12:44 CEST
#            # Note: parse_iso_date do not handle named time zones (CEST)
#            datestr = 'T'.join (L[0].split()[:-1]) # remove last word (and use T as time prefix)
#            return self.parse_iso_date (datestr)
