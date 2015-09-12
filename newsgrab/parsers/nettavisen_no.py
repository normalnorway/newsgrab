""" nettavisen.no

BUG: These to are not consistent! (The first one is wrong)
<meta name="cXenseParse:recs:publishtime" content="2014-09-19T13:20:19.000Z" />
<time class="time_published" datetime="2014-09-19T13:20:19">...</time> 

# Other intereseting data

<meta name="author" content="Camilla Svendsen"/>
<meta property="lp:url" content="http://www.nettavisen.no/dittoslo/her-slar-narkopolitiet-til-pa-videregaende/8487912.html"/>

Uses http://json-ld.org/
"datePublished": "2014-09-19T13:20:19.000Z",    <-- wrong timezone

# Output of probe.py

Meta    title, description, url, type, image, site_name

COUNT   ITEMPROP

Date         : Missing!
"""

from . import OpenGraphParser

class Parser (OpenGraphParser):

    def parse (self):
        meta = super(Parser,self).parse (parse_date=False)

        # Nettavisen bug: cXenseParse:recs:publishtime has zulu time zone
        # wrongly added. Fix: Remove final Z so it's parsed as localtime.
#        datestr = self.get_meta_name ('cXenseParse:recs:publishtime')
#        if datestr[-1] == 'Z': datestr = datestr[:-1]   # hack
#        meta['date'] = self.parse_iso_date (datestr)

        # This one have the correct timezone. God dog!
        lst = self.body.xpath ('.//time[@class="time_published"]/@datetime')
        assert len(lst)==1
        datestr = lst[0]
        meta['date'] = self.parse_iso_date (datestr)

        return meta
