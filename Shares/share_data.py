from sqlalchemy import desc
import urllib
import json


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
    def getalljsonshares(val):
        tempshares = Share.query.order_by(desc(Share.time)).filter(Share.share == val)
        #tempshares = Share.query.order_by(desc(Share.time)).all()

        sharearray = []

        for row in tempshares:

            ticker = row.share
            quote = share_data.JSONSharePrice(ticker)

            sharedata = {
                'symbol': quote['query']['results']['quote']['symbol'],
                'quantity': row.quantity,
                'Price': quote['query']['results']['quote']['LastTradePriceOnly'],
                'Name': quote['query']['results']['quote']['Name']
            }

            sharearray.append(sharedata)

        return sharearray
