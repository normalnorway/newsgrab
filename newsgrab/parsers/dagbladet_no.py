""" dagbladet.no

Uses OpenGraph (missing namespace).

Date: 
<div class="article-date">
  <span class="date">fredag 30. januar 2015</span>,
  <span class="time">kl.10:25</span>
</div>

Date for Dagbladet pluss:
<time datetime="2015-10-16"
      pubdate class="published"
      title="...">...</time>

Notes:
* Does not use html5!
* Dagbladet uses a paywall. Howto detect affected articles?

Other usefull elements:
<link rel="canonical" href="..." />
<meta name="keywords" content="..." />
<meta name="news_keywords" content="..." />
"""

from . import OpenGraphParser

class Parser (OpenGraphParser):
#    charset = 'iso-8859-1'
    fallback_charset = 'iso-8859-1' # used if no charset in Content-Type

    # <p class="article-byline-category">Publisert  den <strong>16. jan 2015,</strong> kl. 07:00 av</p>
    def try_parse_date (self):
        lst = self.body.xpath ('.//p[@class="article-byline-category"]')
        assert len(lst)==1
        assert lst[0].text.startswith ('Publisert')
        L = lst[0].getchildren()
        assert len(L)==1
        strong = L[0]
        assert strong.tag == 'strong'
        datestr = strong.text[:-1].strip()
        timestr = strong.tail
        timestr = timestr.replace('av', '').replace('kl.','').strip()
        return self.parse_date_no (datestr + ' ' + timestr)

    def handle_old_article (self):
        # Old articles like this:
        # http://www.dagbladet.no/kultur/2008/01/29/525270.html
        meta = {}
        meta['title'] = self.get_meta_name ('title')
        meta['description'] = self.get_meta_name ('description')
        meta['url'] = self.url

        # Parse date
        div = self.body.xpath ('//div[@class="published-date"]')[0]
        s = ''.join (div.xpath('text()')).strip()   # get all text
        lst = s.split() # torsdag 14.09.2006 kl. 16:07, oppdatert 16:34
        date = lst[1]
        time = lst[3][:-1]  # strip last char (comma)
        meta['date'] = self.parse_norwegian_date (date+' '+time)

        # Try to get an image
        try:
            div = self.body.xpath ('//div[@id="content"]')[0]
            lst = div.xpath ('//img[@class="pano-image"]')
            meta['image'] = lst[0].attrib['src']
        except:
            pass

        return meta

        # Get date from url. (Note: Can also parse from the text)
#        from urlparse import urlsplit
#        obj = urlsplit (self.url)
#        lst = obj.path.split ('/')
#        date = '-'.join (lst[2:5])
#        meta['date'] = self.parse_iso_date (date + 'T00:00')
#        return meta


    def parse (self):
        meta = super(Parser,self).parse()

        if not 'title' in meta:
            return self.handle_old_article ()

        # http://www.dagbladet.no/2015/07/02/kultur/debatt/meninger/ruspolitikk/sproyterom/39942549/
        L = self.body.xpath ('//p[@class="article-byline-category"]')
        try:
            lst = L[0].xpath ('.//text()')
            # 'Publisert  den ', ' 2. jul 2015,', ' kl. 05:00 av']
            date = lst[1].strip()[:-1]  # strip and remove last ,
            time = lst[2].strip().split()[1]
            dt = self.parse_date_no (date + ' ' + time)
            assert (dt)  # @todo better to let parse_date_no raise on error
            meta['date']= dt
            return meta
        except IndexError:
            pass

        # Dagbladet pluss
        L = self.body.xpath ('//time[@class="published" and @pubdate]')
        if L:
            assert len(L)==1
            timenode = L[0]
            date = timenode.attrib['datetime']
            time = timenode.attrib['title'].split()[3][:-1]
            meta['date'] = self.parse_iso_date (date + 'T' + time)
            # Note: og:url contains postfix (?share=<uuid>)
            # @todo better to strip query string from og:url?
            meta['url'] = self.url
            meta['description'] = self.normalize_space (meta['description'])
            return meta


        # div#articleTools
        # div.article-date > span.date + span.time
        L = self.tree.xpath ("//div[@class='article-date']")
        if not L:
            meta['date']= self.try_parse_date()
        else:
            assert len(L)==1
            elem = L[0]
            e1 = elem.xpath ("span[@class='date']/text()")
            e2 = elem.xpath ("span[@class='time']/text()")
            # e1 = ['fredag 30. januar 2015']
            # e2 = ['kl.10:25']
            datestr = e1[0].split(' ', 1)[1].strip()    # remove first word
            timestr = e2[0].split('.')[1].strip()       # remove kl.
            meta['date'] = self.parse_date_no (datestr + ' ' + timestr)

        return meta
