r""" Forskning.no

Using Open Graph and manual date parsing.

Notes:
* Date element is not very well (semantically) marked
* Date string is not using standard format
* Date string in local timezone

Date markup:
<div class="field field-name-published-date field-type-ds field-label-hidden">
  <div class="field-items">
    <div class="field-item even">28.8 2012 05:00</div>
  </div>
</div>

Other intereseting elements:
<link rel="canonical" href="..." />     <-- using og:url instead
<link rel="shortlink" href="..." />
"""

from . import OpenGraphParser

class Parser (OpenGraphParser):

    def parse (self):
        meta = super(Parser,self).parse()
        xpath = self.body.xpath

        L = xpath('//div[contains(@class, "field-name-published-date")]')
        node = L[0]
        assert 'moscone-container-inner' in node.getparent().attrib['class']

        # Note: Query above returns 4 elements (only wants the first)
        #for node in L: print node.getparent().attrib
        # {'class': 'moscone-container-inner moscone-header-inner panel-panel-inner'}
        # {'class': 'group-metainfo field-group-html-element'}
        # {'class': 'group-metainfo field-group-html-element'}
        # {'class': 'group-metainfo field-group-html-element'}

        datestr = node.xpath("div/div")[0].text.strip()
        meta['date'] = self.strptime (datestr, '%d.%m %Y %H:%M')

        return meta
