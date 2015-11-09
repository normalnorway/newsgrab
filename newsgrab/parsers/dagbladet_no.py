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

    def parse (self):
        meta = super(Parser,self).parse (parse_date=False)

        L = self.body.xpath ('//time[@class="published" and @pubdate]')
        if L:
            assert len(L)==1
            timenode = L[0]
            date = timenode.attrib['datetime']
            time = timenode.attrib['title'].split()[3][:-1]
            meta['date'] = self.parse_iso_date (date + 'T' + time)
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
