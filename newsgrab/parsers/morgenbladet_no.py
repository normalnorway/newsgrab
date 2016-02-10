""" morgenbladet.no

Using Drupal 7 / ramsalt.com

Have og:updated_time but not og:created_time :(

Note: Some articles are missing fields! Like this one:
https://morgenbladet.no/ideer/2016/01/keiserens-nye-narkotikapolitikk
Missing: description & image

The good news? Can also use this parser for articles behind paywall.
"""

from . import OpenGraphParser

class Parser (OpenGraphParser):

    def parse_date (self):
        main = self.body.xpath ('//section[@id="main"]')[0]
        l = main.xpath ('//div[contains(@class, "field-name-published-on")]/text()')
        datetime = ''.join(l).strip()
        time, date = datetime.split(' - ')
        return self.parse_date_no (date + ' ' + time)

    def parse (self):
        meta = super(Parser,self).parse()

        if not 'description' in meta:
            main = self.body.xpath ('//section[@id="main"]')[0]
            lst = main.xpath ('//div[@class="content-main"]//div[contains(@class, "field-name-body")]/p[1]//text()')
            meta['description'] = ''.join (lst)

        if not 'image' in meta:
            meta['image'] = 'https://morgenbladet.no/sites/morgenbladet.no/files/styles/large/public/facebook-cover-image.png'
            # the best we can do for now ...

        return meta
