import re
import logging
from lxml import etree
from datetime import datetime
from newsgrab.dateutils import parse_iso_date

logger = logging.getLogger (__name__)


#def _dict_to_unicode (data, charset):
def _dict_to_unicode (data):
    """Converts all string objects in a dictionary to unicode"""
    out = {}
    charset = 'ascii'
    for key,val in data.iteritems():
        ukey = unicode (key, charset)
        #if isinstance (val, str):
        if type(val) == str:
            uval = unicode (val, charset)
        elif isinstance (val, etree._ElementUnicodeResult):
            uval = unicode (val)    # needed?
        else:
            uval = val
        out[ukey] = uval
    return out


# Helper to parse norwegian dates
# @todo handle seconds in time part (and better error handling)
_RE_DATETIME_PARSE = re.compile (r'(\d{1,2})\. ([a-zA-Z]+) (\d{4}) ?(.*)$')
_MONTH_NAMES = ('januar', 'februar', 'mars', 'april', 'mai', 'juni', 'juli', 'august', 'september', 'oktober', 'november', 'desember')
_MONTH_NAMES_ABBR = ('jan.', 'feb.', 'mars', 'apr.', 'mai', 'juni', 'juli', 'aug.', 'sep.', 'okt.', 'sep.', 'nov.', 'des.')
_MONTH_NAMES_SHORT = [name[:3] for name in _MONTH_NAMES]


def _parse_month_name (name):
    """Parse Norwegian month name"""
    #if name in _MONTH_NAMES_SHORT: return _MONTH_NAMES_SHORT.index (month_name)
    name = name.lower()
    try: return _MONTH_NAMES.index (name) + 1
    except ValueError: pass
    try: return _MONTH_NAMES_SHORT.index (name) + 1
    except ValueError: pass
    try: return _MONTH_NAMES_ABBR.index (name) + 1
    except ValueError: raise ValueError ('Can not parse month name: ' + name)


def _parse_norwegian_datetime (datestr):
    """Parse datetime using Norwegian month names"""
    match = _RE_DATETIME_PARSE.match (datestr)
    try:
        tp = match.groups()[:-1]   # split of last part (time)
        day = int(tp[0])
        month = _parse_month_name (tp[1])
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

#    charset = 'utf-8'
#    http_charset

    def __init__ (self, url=None):
        """If url is None then set_html() must be called"""
        if url: self.set_url (url)

    def set_url (self, url):    # rename load_url?
        self.url = url
        import urllib2
        fp = urllib2.urlopen (url)
        s = fp.headers.get('content-type')
        try:
            self.http_charset = s.split(';')[1].split('=')[-1] if s else None
        except IndexError:
            pass    # note: parser must set self.charset
        self.set_html (fp.read())

    def set_html (self, data):
        #self.tree = etree.HTML (data)
        self.tree = self._create_etree (data)
        lst = [n for n in self.tree if n.tag in ('head', 'body')]
        self.head, self.body = lst[0], lst[1]
        self.meta = None    # clear cache

    def _create_etree (self, data):
        parser = etree.HTMLParser (encoding=self._get_charset())
        return etree.HTML (data, parser=parser)

    def _get_charset (self):
        if hasattr (self, 'charset'):
            return self.charset
        if hasattr (self, 'http_charset'):
            return self.http_charset
        if hasattr (self, 'fallback_charset'):  # hack for dagbladet
            return self.fallback_charset
        raise RuntimeError ('Can not detect encoding. Must set self.charset')

    # Try to parse charset from html
    # Bug: will do case sensitive match for charset (but not http-equiv)
    def _detect_charset (self): # note: not in use anymore
        charset = self.tree.xpath ("/html/head/meta[@charset]/@charset")
        if charset: return charset[0]
        L = self.tree.xpath ("/html/head/meta[translate(@http-equiv,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='content-type']")
        if L: return L[0].get('content').split('=')[-1]
        # Think iso-8859-1 is default for html. But utf-8 is safer these days.
        return 'utf-8'

    def _parse (self):
        return self.parse()

    def parse (self):
        if self.tree is None:
            raise RuntimeError ('No data to parse. Must call set_url(), set_html() or pass url to constructor.')

    ## HELPERS ##

    def get_canonical_link (self):
        L = self.tree.xpath ("/html/head/link[@rel='canonical']/@href")
        assert len(L)==1
        return L[0]

    @staticmethod
    def parse_date_no (datestr):
        """Parse datetime string using Norwegian month names"""
        return _parse_norwegian_datetime (datestr)

    # @todo throw on unparsable input?
    @staticmethod
    def parse_iso_date (datestr):
        return parse_iso_date (datestr.strip())

    @staticmethod
    def parse_norwegian_date (datestr):
        """Parse Norwegian datetime string (dd-mm-yyyy hh:mm[:ss])"""
        try:
            return datetime.strptime (datestr, '%d.%m.%Y %H:%M')
        except ValueError:
            return datetime.strptime (datestr, '%d.%m.%Y %H:%M:%S')

    def get_meta (self, attribute, value):
        """Return the content attribute of all <meta> elements where `attribute` matches `value`"""
        query = "/html/head/meta[@%s='%s']/@content" % (attribute, value)
        return self.tree.xpath (query)

    def get_meta_name (self, name):
        L = self.get_meta ('name', name)
        if len(L) == 1: return L[0]
        s = '<meta name="%s" ... /> elements' % name
        if len(L) == 0: raise RuntimeError ('Not found: ' + s)
        if len(L)  > 1: raise RuntimeError ('Found multiple: ' + s)

    def normalize_space (self, text):
        """Compress multiple whitespaces into one"""
        return self.normalize_space.re.sub (' ', text)
    normalize_space.re = re.compile (r'\s+')


    ## ACCESSORS ##

    def get (self):
        """Get metadata as a dict"""
        if not self.meta:
            #meta = self.parse()
            meta = self._parse()    # XXX
            #del self.tree, self.head, self.body
            #self.tree = None    # release memory
            self.tree = self.head = self.body = None    # release memory
            #self.meta = meta
            self.meta = _dict_to_unicode (meta)  # @todo drop
            # convert all values to unicode? lxml only return
            # unicode strings when needed.
        return self.meta

    def get_json (self):    # get_as_json
        import json
        meta = self.get()
        meta['date'] = str (meta['date']) # json don't handle python datetime
        return json.dumps (meta)



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

    # Strip this from title if set
    title_postfix = None

    # Prefer <link rel="canonical"> over og:url
    use_canonical_url = False

    def _parse (self):
        meta = self.parse()
#        if self.title_postfix:
#            if meta['title'].endswith (self.title_postfix):
#                meta['title'] = meta['title'][0:-len(self.title_postfix)]
        if self.use_canonical_url:
            meta['url'] = self.get_canonical_link ()

        if not 'date' in meta:
            meta['date'] = self.parse_date()  # Q: what if returns None? check nrk parser
        #print meta['date']

        return meta


    def parse (self):
        """Parse OpenGraph properties and return as dict"""
        super(OpenGraphParser,self).parse()
        L = self.tree.xpath ('/html/head/meta[starts-with(@property,"og:")]')
        if not L: return {}

        meta = {}
        for elem in L:
            key = elem.get ('property')[3:] # strip og: prefix
            val = elem.get ('content').strip()
            meta[key] = val

        if meta.has_key ('type') and meta['type'] != 'article':
            logger.info ('og:type = %s for: %s', meta['type'], self.url)

        if hasattr (self, 'strip_title'):
            self.title_postfix = self.strip_title   # alias
        if self.title_postfix:
            if meta['title'].endswith (self.title_postfix):
                meta['title'] = meta['title'][0:-len(self.title_postfix)]

        if 'description' not in meta:
            try: meta['description'] = self.get_meta_name ('description')
            except: pass

        return meta


    def parse_date (self):
        # Try <meta article:published_time>
        datestr = self.get_meta_property ('article:published_time')
        if datestr: return self.parse_iso_date (datestr)

        # Try <time itemprop=datePublished datetime>
        L = self.body.xpath ("//time[@itemprop='datePublished']/@datetime")
        if len(L) == 1:
            return self.parse_iso_date (L[0])
        if len(L) > 1:
            logger.info ('Multiple <time itemprop=datePublished> found, so ignoring all. ' + self.url)

        # Try <time datetime>
        L = self.body.xpath ("//time[@datetime]/@datetime")
        if len(L) > 0:
            if len(L) > 1: logger.warn ('Multiple <time datetime> found. Using the first one. ' + self.url)
            dt = self.parse_iso_date (L[0]) # returns None on parse error
            if dt: return dt
            # Try this format: 2015-10-20 12:12:44 CEST
            # @todo make parse_iso_date handle named time zones
            lst = L[0].split()
            if lst[-1] in ('CEST', 'CET'):
                datestr = 'T'.join (lst[:-1])
                return self.parse_iso_date (datestr)


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
    # @todo rewrite get_meta_* to use this

    def itemprop (self, key, elem=None):
        if elem:
            expr = "//%s[@itemprop='%s']/text()" % (elem, key)
        else:
            expr = "//*[@itemprop='%s']/text()" % key
        #return self.tree.xpath(expr)[0].strip()
        data = self.tree.xpath (expr)
        if len(data) > 1: logger.warn ('More than one match. Ignoring the rest!')
        return data[0].strip()
