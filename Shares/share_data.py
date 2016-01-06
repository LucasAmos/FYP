from sqlalchemy import desc
import urllib
import json
from models import Userownedshare

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
                'name': row.name.name
            }
            sharearray.append(sharedata)

        return sharearray
