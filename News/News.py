import urllib
from xml.etree import ElementTree


class News():

    @staticmethod
    def getNews(ticker):

        base_url = 'http://finance.yahoo.com/rss/headline?s='
        query = ticker

        url = base_url + query
        response = urllib.urlopen(url)
        data = response.read()

        dom = ElementTree.fromstring(data)

        items = dom.findall('channel/item')

        dict ={}

        for item in items:


           # print "**"
           # print item.find('title').text
           # print item.find('link').text

           title = item.find('title').text
           item = item.find('link').text

           dict[title] = item

        return dict











