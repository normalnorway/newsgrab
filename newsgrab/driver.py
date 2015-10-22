"""
@todo rename parserfactory.py?
"""

import os
import logging
from urlparse import urlsplit

logger = logging.getLogger (__name__)


def domain_to_pyid (domain):
    """Convert a domain name into a valid python identifier"""
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain.replace('.', '_').replace('-', '_')

def domain_to_parser_id (domain):
    return domain_to_pyid (domain)


def load_parser (pyid): # get_parser_class?
    """Import a parser module and returns the parser class"""
    try:
        mod = __import__ ('newsgrab.parsers.'+pyid, fromlist=['Parser'])
        return mod.Parser
    except ImportError as ex:
        return None



class ParserFactory (object):
    parsers = {}    # Parser object cache

    # @todo get_by_pyid() or use _get()

    #def get (self, url, load_url=True, urlobj=None):
    def get (self, url, load_url=True):
        urlobj = urlsplit (url)
        pyid = domain_to_parser_id (urlobj.hostname)

        # Try to load from cache
        parser = self.parsers.get (pyid, False)
        if parser: return parser
        # @todo what about load_url?

        # Try to load parser from parsers/<pyid>.py
        try:
            module = __import__ ('newsgrab.parsers.'+pyid, fromlist=['Parser'])
            self.parsers[pyid] = module.Parser (url if load_url else None)
            return self.parsers[pyid]
        except ImportError:
            logger.warning ('No parser found for: ' + urlobj.hostname)

        # No parser found, fall back to OpenGraph parser.
        # @todo can check if it's support (if load_url=True).
        from parsers import OpenGraphParser
        return OpenGraphParser (url if load_url else None)
