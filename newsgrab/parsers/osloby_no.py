''' osloby.no

data-paywall-publishDate="2015-09-10T21:48:50.000Z" data-paywall-ipMode="false">

<time class="published" pubdate="pubdate" datetime="2015-09-10T 21:48+01:00" ...>
<time class="updated"   pubdate="pubdate" datetime="2015-09-11 13:48:22 CEST">
XXX: Time zone not consistent! (CEST is +02:00)

BUG: Time zone is wrong!
Summer time is active for this date ("2015-09-10T 21:48+01:00"), and the
timezone should therefore be +02:00 or CEST.
FIX: But the time is correct, so the fix is to just ignore the wrong tz.

# Output from probe.py

Meta    site_name, image, type, url, title, description

COUNT   ITEMPROP
  3     bestRating
  3     ratingValue
  3     reviewRating
  4     teaserText
  3     worstRating

Date         : Missing!
'''

from . import OpenGraphParser

class Parser (OpenGraphParser):

    def parse (self):
        meta = super(Parser,self).parse()

        lst = self.body.xpath(".//time[@class='published' and @pubdate]/@datetime")
        datestr = lst.pop()
        assert len(lst)==0
        datestr = datestr.replace('\n', '')

        # Bug: Timezone is wrong, so just remove it
        lst = datestr.split('+')
        assert len(lst)==2
        assert lst[1] in ['01:00', '02:00']
        datestr = lst[0]

        meta['date'] = self.parse_iso_date (datestr)

        return meta
