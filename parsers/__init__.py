import logging
from lxml import etree
from datetime import datetime

logger = logging.getLogger (__name__)


# Note: self.tree is released after calling get()
# So additional parsing must be done in the subclass's parse().
class ParserBase (object):
    tree = None     # lxml.etree or None
    url = None      # url passed to ctor (or None)
    meta = None     # cached metadata

    def __init__ (self, url=None):
        """If url is None then set_html() must be called"""
        if url: self.set_url (url)

    def set_url (self, url):
        import urllib2
        self.set_html (urllib2.urlopen(url).read())
        self.url = url

    def set_html (self, data):
        self.tree = etree.HTML (data)
        self.meta = None
        self.url = None
        #self.url = '(none)'

    def parse (self):
        raise NotImplementedError()

    def get (self):
        """Get metadata as a dict"""
        if not self.meta:
            self.meta = self.parse()
            self.tree = None    # release memory
        return self.meta

    def get_json (self):
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
    #namespace = None    # note: not all sites uses this

    def itemprop (self, key, elem=None):
        if elem:
            expr = "//%s[@itemprop='%s']/text()" % (elem, key)
        else:
            expr = "//*[@itemprop='%s']/text()" % key
        #return self.tree.xpath(expr)[0].strip()
        data = self.tree.xpath (expr)
        if len(data) > 1:
            logger.warn ('More than one match. Ignoring the rest!')
        return data[0].strip()


    def parse (self):
        """Parse OpenGraph properties and return as dict"""
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

        # @todo these transformations don't belong here
        # @todo nuke all unknown keys?
        meta.pop ('type', None)
        meta.pop ('site_name', None)
        meta['summary'] = meta.pop ('description', '')
        return meta


    def parse_date (self, fmt='%Y-%m-%dT%H:%M:%S'):
        datestr = self.itemprop ('datePublished')
        assert datestr
        return datetime.strptime (datestr, fmt)
        # Note: %T is not supported in Python :(

#    def _parse_date (self, datestr, fmt):
#        return datetime.strptime (datestr, fmt)

    def is_supported (self):
        return self.is_supported

    """
    def _parse_namespace (self):
        self.namespace = self.tree.xpath('/html')[0].get('xmlns:og')
        if not self.namespace:
            logger.info('fixme')
            return
        if self.namespace != 'http://ogp.me/ns#':
            logger.warn('fixme')
    """
