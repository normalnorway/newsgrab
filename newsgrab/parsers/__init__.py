import re
import logging
from lxml import etree
from datetime import datetime
from datetime import timedelta

logger = logging.getLogger (__name__)


def last_sunday_of_month (year, month):
    """Return day number of last sunday in the month.
       Stolen from http://stackoverflow.com/a/29338804"""
    import calendar
    obj = calendar.monthcalendar (year, month)
    return max (obj[-1][calendar.SUNDAY], obj[-2][calendar.SUNDAY])

# XXX note dt is in zulu time. must fix cutoff
def is_dst (dt):
    """Return true if daylight saving time is in effect"""
    assert (dt.year >= 1980)
    if dt.month < 3:  return False  # mars
    if dt.month > 10: return False  # oktober
    if dt.month in [3,10]:
        cutoff = dt.replace (day = last_sunday_of_month (dt.year, dt.month),
                             hour=2, minute=0, second=0)
        if dt.month ==  3: return dt >= cutoff
        if dt.month == 10: return dt < cutoff # xxx correct time: 03:00
    return True

#from datetime import datetime
#dt = datetime (2015, 10, 25, 01, 59)
#print dt
#print is_dst (dt)
#exit (0)



def _dict_to_unicode (data, charset):
    """Converts all string objects in a dictionary to unicode"""
    out = {}
    for key,val in data.iteritems():
        ukey = unicode (key, charset)
        if type(val) == str:
            uval = unicode (val, charset)
        else:
            uval = val
        out[ukey] = uval
    return out


# Helper to parse norwegian dates
# @todo handle abbreviated month names
# @todo handle seconds in time part (and better error handling)
_RE_DATETIME_PARSE = re.compile (r'(\d{1,2})\. ([a-zA-Z]+) (\d{4})(.*)')
_MONTH_NAMES = (None, 'januar', 'februar', 'mars', 'april', 'mai', 'juni', 'juli', 'august', 'september', 'oktober', 'november', 'desember')
_ABMONTH_NAMES = (None, 'jan.', 'feb.', 'mars', 'apr.', 'mai', 'juni', 'juli', 'aug.', 'sep.', 'okt.', 'sep.', 'nov.', 'des.')

def _parse_norwegian_datetime (datestr):
    """Parse datetime using Norwegian month names"""
    match = _RE_DATETIME_PARSE.match (datestr)
    tp = match.groups()[0:-1]   # split of last part (time)
    try:
        day = int(tp[0])
        month = _MONTH_NAMES.index(tp[1].lower())
        year = int(tp[2])
    except ValueError as ex:
        raise ValueError ('Can not parse date: %s [%s]' % (' '.join(tp), str(ex)))

    timestr = match.groups()[-1].strip()
    if timestr:
        tp = timestr.split(':')
        hour = int(tp[0])
        minute = int(tp[1])
    else:
        hour, minute = 0,0  # missing, so use 00:00

    return datetime (year, month, day, hour, minute)



# Note: self.tree is released after calling get()
# So additional parsing must be done in the subclass's parse().
class ParserBase (object):
    url = None      # url passed to ctor (or None)
    tree = None     # lxml.etree or None    (@todo rename root?)
    head = None     # lxml.etree._Element of html head
    body = None     # lxml.etree._Element of html body
    meta = None     # cached metadata

    def __init__ (self, url=None):
        """If url is None then set_html() must be called"""
        if url: self.set_url (url)

    # @todo rename set -> load
    def set_url (self, url):
        import urllib2
        self.set_html (urllib2.urlopen(url).read())
        self.url = url

    def set_html (self, data):
        self.tree = etree.HTML (data)
        self.head = self.tree.xpath ('/html/head[1]')[0]
        self.body = self.tree.xpath ('/html/body[1]')[0]
#        self.head = self.tree[0]   # note: can be comment
#        self.body = self.tree[1]
#        assert self.head.tag == 'head'
#        assert self.body.tag == 'body'
#        print len(tree)     # 3
#        print tree[0].tag   # <built-in function Comment>

    #def set_html_file (self, filename):

    # Bug: will do case sensitive match for charset and http-equiv
    def _detect_charset (self):
        charset = self.tree.xpath ("/html/head/meta[@charset]/@charset")
        if charset: return charset[0]
        #for elem in self.tree.xpath ("/html/head/meta"):
        L = self.tree.xpath ("/html/head/meta[translate(@http-equiv,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='content-type']")
        if L: return L[0].get('content').split('=')[-1]
        logger.warn ('Missing charset for "%s", defaulting to latin1', self.url)
        return 'iso-8859-1' # default for html
        # @todo try to detect it? then must store htmldata
        #chardet.detect()

    def parse (self):
        if self.tree is None:
            raise Exception ('No data to parse. Must call set_url(), set_html() or pass url to constructor.')
        self.charset = self._detect_charset()

    ## Helpers

    def get_canonical_link (self):
        L = self.tree.xpath ("/html/head/link[@rel='canonical']/@href")
        assert len(L)==1
        return L[0]

    def parse_date_no (self, datestr):
        """Parse datetime string using Norwegian month names"""
        return _parse_norwegian_datetime (datestr)

    # @todo throw DateParsingError?
    def parse_iso_date (self, datestr): # @todo return_in_utc=False
        """Parse a ISO 8601 combined date and time"""
        if datestr[-1] == 'Z':
            datestr = datestr[:-1] + '+00:00'

        # Note: Time zones in ISO 8601 are represented as local time when
        # no time zone is given. While it may be safe to assume local time
        # when communicating in the same time zone, it is ambiguous when
        # used in communicating across different time zones.
        # https://en.wikipedia.org/wiki/ISO_8601#Time_zone_designators

        match = re.match (r'(.*)([+-])(\d\d):?(\d\d)?$', datestr)
        #print match.groups()
        # ('2014-03-07T06:00:24', '+', '01', None)
        if match:
            # \1    2014-03-07T06:00:24
            # \2    +
            # \3    01
            # \4    00
            #tz_idx = match.regs[1][0]   # start pos of first match
            #dt = datetime.strptime (datestr[:idx], '%Y-%m-%dT%H:%M:%S')
            dt = datetime.strptime (match.expand(r'\1'), '%Y-%m-%dT%H:%M:%S')
            dt = dt.replace (second=0)
            tz_hour = int (match.expand(r'\2\3'))
            tz_min  = int (match.expand(r'\4')) if match.lastindex==4 else 0
            return dt + timedelta (hours=tz_hour, minutes=tz_min)
        assert False    # XXX

    # q: need return_in_utc?
    def parse_iso_date_new (self, datestr, return_in_utc=False):
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


    ## Accessors

    def get (self):
        """Get metadata as a dict"""
        if not self.meta:
            meta = self.parse()
            #del self.tree, self.head, self.body
            #self.tree = None    # release memory
            self.tree = self.head = self.body = None    # release memory
            self.meta = _dict_to_unicode (meta, self.charset)
        return self.meta

    def get_json (self):    # get_as_json
        import json
        meta = self.get()
        meta['date'] = str (meta['date']) # json don't handle python datetime
        return json.dumps (meta)




# TODO:
# - helper that checks if all vital metadata is there
# - A tag can have multiple values, just put multiple versions of
#   the same <meta> tag on your page.

class OpenGraphParser (ParserBase):
    """Parse Open Graph protocol metadata - http://ogp.me/

    Will parse all OpenGraph meta tags inside html > head.
    Example: <meta property="og:title" content="Some title">

    The four required properties for every page are:
    og:title, og:type, og:image, og:url

    Optional Metadata: og:description, og:site_name

    If og:type is article, then the following properties should/might
    be available: http://ogp.me/#type_article
    Unfortunately these are not well supported by Norwegian newspapers.
    """

    supported = False

    def itemprop (self, key, elem=None):
        if elem:
            expr = "//%s[@itemprop='%s']/text()" % (elem, key)
        else:
            expr = "//*[@itemprop='%s']/text()" % key
        #return self.tree.xpath(expr)[0].strip()
        data = self.tree.xpath (expr)
        if len(data) > 1: logger.warn ('More than one match. Ignoring the rest!')
        return data[0].strip()


    def parse (self):
        """Parse OpenGraph properties and return as dict"""
        super(OpenGraphParser,self).parse()
        L = self.tree.xpath ('/html/head/meta[starts-with(@property,"og:")]')
        if not L: return {}
        self.supported = True

        meta = {}
        for elem in L:
            key = elem.get ('property')[3:] # strip og: prefix
            val = elem.get ('content').strip()
            meta[key] = val

        if meta.has_key ('type') and meta['type'] != 'article':
            logger.info ('og:type = %s for: %s', meta['type'], self.url)

        # Try to parse 'datePublished'
        # @todo move to parse.date()?
        L = self.tree.xpath ("//*[@itemprop='datePublished']/text()")
        if len(L) == 1:
            datestr = L[0].strip()
            for fmt in ('%d.%m.%Y %H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S'):
                try:
                    meta['date'] = datetime.strptime (datestr, fmt)
                    break
                except ValueError:
                    pass
            if not meta.has_key('date'):
                logger.info ('Have datePublished, but unable to parse date: %s', datestr)
                # XXX but using text(), also try datetime attrib
                #     http://www.ba.no/apen-om-eget-rusmisbruk/s/5-8-146941
        elif len(L) > 1:
            logger.info ('Found multiple datePublished; do not know howto handle')

        return meta


    # Deprecated: Better to add the date format to parse()
    def parse_date (self, fmt='%Y-%m-%dT%H:%M:%S'):
        logger.warn ('parse_date() is deprecated!')
        datestr = self.itemprop ('datePublished')
        assert datestr
        return datetime.strptime (datestr, fmt)
        # Note: %T is not supported in Python :(

    def is_supported (self):
        return self.is_supported

    ## Helpers available for parsers

    def strptime (self, datestr, fmt):
        """Helper so parsers don't have to include datetime"""
        return datetime.strptime (datestr, fmt)

    def get_meta_property (self, prop_name): # @todo default=None or allow_empty
        """"<meta property="prop_name" content="returns-this-value" />"""
        L = self.head.xpath (".//meta[@property='%s']/@content" % prop_name)
        if len(L) == 0: return None
        if len(L) == 1: return L[0]
        raise RuntimeError ('found multiple <meta name="%s" ... /> elements' % prop_name)
