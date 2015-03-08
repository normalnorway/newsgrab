# encoding: utf-8
'''
forskning.no

<html  lang="nb" dir="ltr" prefix="og: http://ogp.me/ns#">

Missing: og:description

<link rel="canonical" href="..." />

Note: Not equal to "ingress"
<meta name="twitter:description" content="..." />

div#content
h1.title
div.field-name-field-intro-text
div.field-published-date
'''

from datetime import datetime
from . import OpenGraphParser

class Parser (OpenGraphParser):

    def parse (self):
        meta = super(Parser,self).parse()
        xpath = self.tree.xpath

        # Date
        tmp = xpath('//div[contains(@class, "field-name-published-date")]')[0]
        tmp = tmp.xpath("div/div")[0].text.strip()
        meta['date'] = datetime.strptime(tmp, '%d.%m %Y %H:%M')

        # Description
        tmp = xpath('//div[contains(@class, "field-name-field-intro-text")]')[0]
        meta['description'] = tmp.xpath("div/div/p")[0].text.strip()

        return meta
