import logging
from lxml import etree
from datetime import datetime

logger = logging.getLogger (__name__)


class ParserBase (object):
    tree = None     # lxml.etree or None
    url = None      # url passed to ctor (or None)
    meta = None     # cached metadata

    def __init__ (self, url=None):
        '''If url is None then set_html() must be called'''
        if url: self.set_url (url)

    def set_url (self, url):
        import urllib2
        self.set_html (urllib2.urlopen(url).read())
        self.url = url

    def set_html (self, data):
        self.tree = etree.HTML (data)
        self.url = '(none)'

    def parse (self):
        raise NotImplementedError()

    def get (self):
        '''Get metadata as a dict'''
        if not self.meta:
            self.meta = self.parse()
            self.tree = None    # release memory
        return self.meta

    def get_json (self):
        import json
        meta = self.get()
        meta['date'] = str (meta['date'])
        return json.dumps (meta)



class OpenGraphParser (ParserBase):
    '''Parse Open Graph protocol metadata - http://ogp.me/'''

    def itemprop (self, key, elem=None):
        if elem:
            expr = "//%s[@itemprop='%s']/text()" % (elem, key)
        else:
            expr = "//*[@itemprop='%s']/text()" % key
        return self.tree.xpath(expr)[0].strip()
        # @todo warn if multiple elements matches? use itemprops for that?


    def date (self):    # @todo parse_data || get_date
        datestr = self.itemprop ('datePublished')
        return datetime.strptime (datestr, '%Y-%m-%dT%H:%M:%S')
        # %T is equivalent to %H:%M:%S
        # ... but not supported in Python :(


    def parse (self):
        # @todo assert that all metadata is there. if not check itemprop
        #assert self.is_supported()  # @todo warn instead?
        L = self.tree.xpath ('/html/head/meta[starts-with(@property,"og:")]')
        #return dict (e.values() for e in L)
        meta = dict( (e.values()[0][3:],e.values()[1]) for e in L ) # strip og: prefix from keys
        if not meta:
            return None
        if meta.get('type','') != 'article':
            logger.warning ('Ignoring og:type=%s for: %s', meta.get('type'), self.url)
            return None
        # @todo better to nuke all unknown keys?
        meta.pop ('type', None)
        meta.pop ('site_name', None)
        meta['summary'] = meta.pop ('description', '')
        return meta


    # @note abcnyheter uses meta.property=og:* but don't have xmlns,
    #       so better to check for any og: tags
    # @todo function that returns supported og: tags
    def is_supported (self):
        return self.tree.xpath('/html')[0].get('xmlns:og') == 'http://ogp.me/ns#'
