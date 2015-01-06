import os
import logging
from urlparse import urlparse

logger = logging.getLogger (__name__)

# Did not find a way to __import__ modules relative to current
# directory, so must add current dir to python's path instead.
import sys
sys.path.append (os.path.dirname (__file__))


def domain_to_pyid (domain):
    '''Convert a domain name into a valid python identifier'''
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain.replace('.', '_')


class ParserFactory (object):
    parsers = {}    # Parser object cache

    def get (self, url, load_url=True):
        #pyid = domain_to_pyid (urlparse(url).netloc)
        urlobj = urlparse(url)
        pyid = domain_to_pyid (urlobj.netloc)
        parser = self.parsers.get (pyid, False)
        if parser:
            return parser

        # Try to load parser from parsers/<pyid>.py
        try:
            module = __import__ ('parsers.'+pyid, fromlist=['Parser'])
            assert module
            self.parsers[pyid] = module.Parser (url if load_url else None)
            return self.parsers[pyid]
        except ImportError:
            pass

        logger.warning ('No parser found for: ' + urlobj.netloc)

        # No parser found, fall back to OpenGraph parser.
        # @todo can check if it's support (if load_url=True).
        from parsers import OpenGraphParser
        return OpenGraphParser (url if load_url else None)
