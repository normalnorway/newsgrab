""" tidsskriftet.no - Tidsskriftet for Den norske legeforening

Server: Apache
X-Powered-By: eZ Publish

BUG: The webserver uses Content-Encoding: gzip, even when the client
does not ask for it! This is erroneous behavious. Shame on you :)

Note: og:image defaults to http://tidsskriftet.no/image/currentcover.jpg,
which is freaking huge.
"""

from . import OpenGraphParser

class Parser (OpenGraphParser):

    # Work around bug described above
    def set_url (self, url):
        import urllib2
        fp = urllib2.urlopen (url)
        if fp.headers.get('content-encoding') == 'gzip':
            from io import BytesIO
            from gzip import GzipFile
            buf = BytesIO (fp.read())
            html = GzipFile (fileobj=buf).read()
        else:
            html = fp.read()
        ct = fp.headers.get('content-type')
        self.http_charset = ct.split(';')[1].split('=')[-1]
        self.set_html (html)
        self.url = url


    def parse (self):
        meta = super(Parser,self).parse()

        p = self.body.xpath ('//article/div[@id="sammendrag"]/p[1]')[0]
        meta['description'] = ''.join (p.itertext())

        node = self.body.xpath ('//section[@id="content"]/aside[@id="ifooter"]/div[@class="meta"]/a[1]')[0]
        lst = node.text.split()     # Nr. 5 -  1. mars 2007
        datestr = ' '.join (lst[-3:])
        meta['date'] = self.parse_date_no (datestr)

        # og:image has an random unique id appended:
        # http://tidsskriftet.no/image/currentcover.jpg?cache=<random-id>
        # This change for each request, so must remove it so the
        # test fixture don't break.
        import urlparse
        url = meta['image']
        obj = urlparse.urlsplit (url)
        meta['image'] = urlparse.urljoin (url, obj.path)
        # @todo create helper: url_remove_querystring / clean_url
        # better way: url = url[:url.find('?')]

        return meta
