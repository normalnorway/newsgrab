""" t-a.no -- Tronder-Avisa

<time class="published" datetime="2015-07-11 11:19"><span class="label">Publisert:</span> 11.07.2015 11:19</time>
<time class="modified" datetime="2015-07-11 11:24"><span class="label">Sist endret:</span> 11.07.2015 11:24</time>
"""

from . import OpenGraphParser

class Parser (OpenGraphParser):

    def parse (self):
        meta = super(Parser,self).parse()
        
        L = self.body.xpath ("//div[@id='content']//div[@class='lead']/text()")
        assert len(L)==1
        meta['description'] = L[0].strip()

        return meta
