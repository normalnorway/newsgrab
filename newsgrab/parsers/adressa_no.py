""" Adresseavisen AS - adressa.no

<time class="published" datetime="2015-09-11 08:58">
  <span class="label">Publisert:</span> 11 september 2015 08:58
</time>

<meta property="article:published_time" content="2015-09-11T08:58:28+01:00"/>
<meta property="article:modified_time" content="2015-09-11T15:29:33+01:00"/>
BUG: Timezone is wrong :(

<meta name="description" content="..." />

<div class="mainLead positiveBottom"><div class="lead">description</div></div>
<meta name="keywords" content="comma-separated-list" />
<meta name="author" property="article:author" content="Tiril Vik Nordeide"/>
"""

from . import OpenGraphParser

class Parser (OpenGraphParser):
    pass

#        lst = self.body.xpath ('.//time[@class="published"]/@datetime')
#        assert len(lst) == 1
#        datestr = lst[0]
#        meta['date'] = self.strptime (datestr, '%Y-%m-%d %H:%M')

        # Note: Time zone is wrong for summer time, but don't matter
        # since it's just ignored (and assumed to be in local time).
