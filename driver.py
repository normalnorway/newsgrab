import os
from urlparse import urlparse


def domain_to_pyid (domain):
    '''Convert a domain name into a valid python identifier'''
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain.replace('.', '_')


class ParserFactory (object):
    parsers = {}

    def get (self, url, load=True):
#        domain = urlparse(url).netloc
#        if domain.startswith('www.'):
#            domain = domain[4:]
#        pyid = domain.replace('.', '_')
        pyid = domain_to_pyid (urlparse(url).netloc)
        parser = self.parsers.get (pyid, False)
        if parser:
            print 'hit', parser
            return parser
        basedir = os.path.dirname (__file__)
        if os.path.exists (os.path.join (basedir, 'parsers', pyid+'.py')):
            module = __import__ ('parsers.'+pyid, fromlist=['Parser'])
            if not load: url = None
            self.parsers[pyid] = parser = module.Parser (url)
            return parser

        # No parser found, try OpenGraph parser
        # @todo check for og support: parser.is_supported()
        from parsers import OpenGraphParser
        print 'XXX'
        return OpenGraphParser()
