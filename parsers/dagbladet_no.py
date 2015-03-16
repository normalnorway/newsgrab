""" dagbladet.no

Uses OpenGraph (missing namespace).

Date: 
<div class="article-date">
  <span class="date">fredag 30. januar 2015</span>,
  <span class="time">kl.10:25</span>
</div>

probe.py:
  Meta    title, url, image, type, site_name, description

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

    def parse (self):
        meta = super(Parser,self).parse()

        # div#articleTools
        # div.article-date > span.date + span.time
        L = self.tree.xpath ("//div[@class='article-date']")
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
