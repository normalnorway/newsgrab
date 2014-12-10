''' Aftenposten.no

Uses OpenGraph + <time> element.

xmlns:fb="http://www.facebook.com/2008/fbml"
xmlns:og="http://ogp.me/ns#">
'''

from datetime import datetime, timedelta
from . import OpenGraphParser


class Parser (OpenGraphParser):
    def parse (self):
        meta = super(Parser,self).parse()

        # div.dateline > span.date > time.published
        tmp = self.tree.xpath ('//div[contains(@class,"dateline")]/span/time[@class="published" and @pubdate="pubdate"]/@datetime')[0]
        tmp = tmp.strip()   # needed?
        tmp = tmp.replace ('\n', '')
        date = datetime.strptime (tmp[:-6], '%Y-%m-%dT%H:%M')
        #tz = tmp[-6:]
        #date -= timedelta (seconds = int (tz[:3]) * 3600) # to utc
        meta['date'] = date

        return meta
