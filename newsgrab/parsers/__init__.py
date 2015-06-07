import re
import logging
from lxml import etree
from datetime import datetime

logger = logging.getLogger (__name__)


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
    tree = None     # lxml.etree or None
    url = None      # url passed to ctor (or None)
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
        self.meta = None
        self.url = None

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

    def parse_date_no (self, datestr):
        """Parse datetime string using Norwegian month names"""
        return _parse_norwegian_datetime (datestr)

    def get (self):
        """Get metadata as a dict"""
        if not self.meta:
            meta = self.parse()
            self.tree = None    # release memory
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


    #def getmetaprop (tree, key):
    #    return tree.xpath("/html/head/meta[@property='%s']/@content" % key)[0]

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

#    def _parse_date (self, datestr, fmt):
#        return datetime.strptime (datestr, fmt)

    def is_supported (self):
        return self.is_supported
