# encoding: utf-8
""" kjendis.no

HTTP Content-Type does *not* contain charset. Can parse this:
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>

<time>søndag 15. november 2015</time>

<div class="published">
  Publisert <time class="created">01.02.2011, kl. 12:40</time>
</div>

<meta name="keywords" content="narkotika,hasj,legalisering,norske_kjendiser,kjendis" />
"""

from . import OpenGraphParser

class Parser (OpenGraphParser):
    charset = 'iso-8859-1'

    def parse_date (self):
        L = self.body.xpath ('//div[@class="published"]/time')
        if not L: return
        assert len(L)==2
        ds1 = L[0].xpath ('text()')
        ds2 = L[0].xpath ('text()')
        assert ds1 == ds2

        # '01.02.2011, kl. 12:40'
        s = ''.join (ds1).strip()
        lst = s.split()
        date = lst[0][:-1]      # remove last comma
        time = lst[2]

        return self.parse_norwegian_date (date + ' ' + time)
