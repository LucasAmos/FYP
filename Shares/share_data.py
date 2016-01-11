from sqlalchemy import desc
import urllib
import json
from models import Userownedshare
#testttttt
class share_data():

    @staticmethod
    def JSONSharePrice(ticker):

        base_url = 'https://query.yahooapis.com/v1/public/yql?'
        query = {
        'q': 'select LastTradePriceOnly, symbol, Name from yahoo.finance.quote where symbol in ("%s","")' %ticker,
        'format': 'json',
         'env': 'store://datatables.org/alltableswithkeys'
         }

        url = base_url + urllib.urlencode(query)
        response = urllib.urlopen(url)
        data = response.read()
        quote = json.loads(data)

        return quote


    @staticmethod
    def getalljsonshares(user):
        tempshares = Userownedshare.query.order_by(desc(Userownedshare.ticker)).filter(Userownedshare.user == user)

        sharearray = []

        for row in tempshares:

            ticker = row.ticker
            quote = share_data.JSONSharePrice(ticker)

            sharedata = {
                'symbol': quote['query']['results']['quote']['symbol'],
                'quantity': row.quantity,
                'price': quote['query']['results']['quote']['LastTradePriceOnly'],
                #'name': quote['query']['results']['quote']['Name']
                'name': row.name.name,
                'id': row.id
            }
            sharearray.append(sharedata)

        return sharearray


    @staticmethod
    def getportfoliovalue(user):
        tempshares = Userownedshare.query.order_by(desc(Userownedshare.ticker)).filter(Userownedshare.user == user)

        sharearray = []

        sharevalue = 0.0
        dividends = 0.0
        portfoliovalue = 0.0

        for row in tempshares:

            ticker = row.ticker
            quote = share_data.JSONSharePrice(ticker)

            shareprice = float (quote['query']['results']['quote']['LastTradePriceOnly'])
            quantity = row.quantity
            shareholding = shareprice * quantity
            dividends = dividends + row.dividends
            sharevalue += shareholding
            portfoliovalue = sharevalue + dividends

        sharearray.append(sharevalue)
        sharearray.append(dividends)
        sharearray.append(portfoliovalue)
        dictvalues = {'portfoliovalue': portfoliovalue, 'sharevalue': sharevalue, 'dividends': dividends}

        return dictvalues
