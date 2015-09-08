""" Bergensavisen - www.ba.no

@todo use these instead
<meta property="article:published_time" content="2015-09-03T15:29:30.000Z" />
<meta property="article:modified_time" content="2015-09-03T18:14:03.000+0200" />
Note: Time zone is not consistent :(

<meta property="og:type" content="story" />

Note: 'og:url' has query parameters appended. Strip or use rel=canonical.

<link rel="canonical" href="http://www.ba.no/apen-om-eget-rusmisbruk/s/5-8-146941" />
"""

from . import OpenGraphParser

# @todo only compile regex once
# @todo improve datePublished in parse(); then can drop date handling here?


def get_itemprops (node, itemprop, element='*'):
    return node.xpath (".//%s[@itemprop='%s']" % (element, itemprop))

def get_itemprop (node, itemprop, element='*'):
    L = get_itemprops (node, itemprop, element)
    if len(L) == 0: return None     # Not found
    if len(L) == 1: return L[0]     # Found one entry
    assert False                    # Found multiple entries

def get_date_published (root, element='time'):
    node = get_itemprop (root, 'datePublished', element)
    return node.attrib['datetime']  # note: will raise KeyError
    #return node.get ('datetime', None)

def get_date_modified (root, element='time'):
    return get_itemprop (root, 'dateModified', element).attrib['datetime']

# get_published_date?

import re
from datetime import timedelta

class Parser (OpenGraphParser):

    def parse (self):
        meta = super(Parser,self).parse()
        body = self.body

        L = body.xpath (".//main/article[@itemtype='http://schema.org/Article']")
        assert len(L) == 1
        article = L.pop()

        # og:url has (unwanted) query parameters appended, so don't use
        # @todo can set OpenGraph.use_canonical instead?
        meta['url'] = self.get_canonical_link ()

        # Published date
        # Can't to this; wrong timezone
        #meta['date'] = get_date_published (body)
        #meta['date_utc'] = get_date_published (body)

        # Note: datePublished is in zulu time, and it's not possible to
        # convert to local time (Norwegian) by blindly adding the
        # time-zone difference ('cause daylight savings).
        # The solution is to use a timezone aware library (like pytz).

        # But dateModified is in the norwegian time zone, and as long as
        # there are no daylight savings shift between the publishedDate
        # and the modifiedDate, then can use this workaround: Get timezone
        # offset from dateModified and add that to datePublished.

        date_str = get_date_published (body)
        assert date_str[-1] == 'Z'  # assert zulu time
        dt = self.parse_iso_date_new (date_str)

        match = re.match (r'(.*)([+-])(\d\d):?(\d\d)?$', get_date_modified (body))
        assert match

        tz_hour = int (match.expand(r'\2\3'))
        tz_min  = int (match.expand(r'\4')) if match.lastindex==4 else 0
        dt += timedelta (hours=tz_hour, minutes=tz_min)

        meta['date'] = dt
        return meta
