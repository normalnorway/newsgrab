""" klassekampen.no """

from . import OpenGraphParser

class Parser (OpenGraphParser):

    def parse_date (self):
        L = self.body.xpath ("//div[@class='main-titles']/*[1]") # first-child
        div = L.pop()
        assert not L
        datestr = div.text.split(' ', 1)[1]
        return self.parse_date_no (datestr)
