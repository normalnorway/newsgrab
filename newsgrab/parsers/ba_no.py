""" Bergensavisen - www.ba.no

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

def get_canonical_link (root):
    L = root.xpath ("/html/head/link[@rel='canonical']/@href")
    assert len(L)==1
    return L[0]


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



# XXX debug (parse_iso_date_2)
import re
from datetime import datetime, timedelta


class Parser (OpenGraphParser):

    def parse_iso_date_2 (self, datestr, return_in_utc=False):
        if datestr[-1] == 'Z':
            datestr = datestr[:-1] + '+00:00'

        # Regex capture groups
        # g0    datetime-part
        # g1    datetime-part, fraction of seconds (ignored)
        # g2    timezone: + or -
        # g3    timezone: hours
        # g4    timezone: minutes (optional)

        match = re.match (r'(.*)(?:\.\d{3})([+-])(\d\d):?(\d\d)?$', datestr)
        if not match: return None

#        print match.groups()
        # \1    2014-03-07T06:00:24
        # \2    +
        # \3    01
        # \4    00

        dt = datetime.strptime (match.expand(r'\1'), '%Y-%m-%dT%H:%M:%S')
        dt = dt.replace (second=0)  # nuke seconds
        if return_in_utc:
            tz_hour = int (match.expand(r'\2\3'))
            tz_min  = int (match.expand(r'\4')) if match.lastindex==4 else 0
            dt += timedelta (hours=tz_hour, minutes=tz_min)
        return dt


    def parse (self):
        meta = super(Parser,self).parse()

        # @todo move to parent ctor
        head = self.tree[0]
        body = self.tree[1]
        assert head.tag == 'head'
        assert body.tag == 'body'

        L = body.xpath (".//main/article[@itemtype='http://schema.org/Article']")
        assert len(L) == 1
        article = L.pop()

        # og:url has (unwanted) query parameters appended, so don't use
        meta['url'] = get_canonical_link (head)

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
        dt = self.parse_iso_date_2 (date_str)

        match = re.match (r'(.*)([+-])(\d\d):?(\d\d)?$', get_date_modified (body))
        assert match

        tz_hour = int (match.expand(r'\2\3'))
        tz_min  = int (match.expand(r'\4')) if match.lastindex==4 else 0
        dt += timedelta (hours=tz_hour, minutes=tz_min)

        meta['date'] = dt
        return meta
