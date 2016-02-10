""" morgenbladet.no

Using: Drupal 7 / ramsalt.com

Have og:updated_time but not og:created_time

Note: Some articles are missing fields! Like this one:
https://morgenbladet.no/ideer/2016/01/keiserens-nye-narkotikapolitikk
Missing: description & image
"""

from . import OpenGraphParser

class Parser (OpenGraphParser):

    def parse_date (self):
        main = self.body.xpath ('//section[@id="main"]')[0]
        l = main.xpath ('//div[contains(@class, "field-name-published-on")]/text()')
        datetime = ''.join(l).strip()
        time, date = datetime.split(' - ')
        return self.parse_date_no (date + ' ' + time)
