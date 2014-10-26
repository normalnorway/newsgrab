# encoding: utf-8
'''
forskning.no

<link rel="canonical" href="http://forskning.no/2014/10/hvor-farlig-er-cannabisbruk" />

<meta property="og:image" content="http://forskning.no/sites/forskning.no/files/201052_hasj_None.jpg" />
<meta property="og:title" content="Slik skader cannabis" />

@note not equal to ingress
<meta name="twitter:description" content="Om cannabis skal legaliseres har vært et hett debattema i mange land den siste tiden, også i Norge. Nå har den australske forskeren Wayne Hall gått igjennom mye av forskningen siden 1993 som tar for seg usunne og helseskadelige konsekvenser av cannabisbruk.  Oversikten til Wayne Hall tar både for seg negative konsekvenser av kronisk bruk av cannabis, og eventuelle konsekvenser av sjeldent bruk, eller bare å bruke cannabis én gang. Ifølge Halls forskning øker cannabisbruk blant annet risikoen for alvorlige ulykker og psykiske lidelser som schizofreni." />

div#content
h1.title
div.field-name-field-intro-text
div.field-published-date
'''

from datetime import datetime
from . import ParserBase


def getmetaprop (tree, key):
    return tree.xpath("/html/head/meta[@property='%s']/@content" % key)[0]


class Parser (ParserBase):
    def __str__ (self):
        return 'abcnyheter.no'

    def parse (self):
        data = dict()
        tree = self.tree

        tmp = tree.xpath('//div[contains(@class, "field-name-published-date")]')[0]
        tmp = tmp.xpath("div/div")[0].text.strip()
        data['date'] = datetime.strptime(tmp, '%d.%m %Y %H:%M')

        data['title'] = getmetaprop (tree, 'og:title')

        tmp = tree.xpath('//div[contains(@class, "field-name-field-intro-text")]')[0]
        data['summary'] = tmp.xpath("div/div/p")[0].text.strip()

        data['image'] = getmetaprop (tree, 'og:image')

        return data


'''
def getdiv (elem, key, subpath='div/div', extra=None):
    tmp = elem.xpath('//div[contains(@class, "field-%s")]' % key)[0]
    if extra: subpath += '/' + extra
    return tmp.xpath (subpath)[0].text.strip()
print getdiv (tree, 'name-field-intro-text')
'''
