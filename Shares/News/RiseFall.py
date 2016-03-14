import urllib
from xml.etree import ElementTree
from Shares.models import Userownedshare
from sqlalchemy import desc
from Shares.share_data import share_data


class RiseFall():

    @staticmethod
    def getTickers(user):

        tickers = Userownedshare.query.order_by(desc(Userownedshare.ticker)).filter_by(user=user)

        tickerset = set()
        for item in tickers:
            tickerset.add(item.ticker + ".L")

        return tickerset

    @staticmethod
    def getRiseFall(user):

            ticker = RiseFall.getTickers(user)

            data = share_data.JSONShareFall(ticker)

            return data['query']['results']['quote']







