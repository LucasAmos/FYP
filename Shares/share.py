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