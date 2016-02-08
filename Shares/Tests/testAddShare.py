from flask.ext.testing import TestCase
from flask import Flask
from Shares import db, app as appy
from Shares.models import User, Userownedshare, Share
from testDatabase import test

import manage


class test(TestCase):

    def create_app(self):
        appy.config['TESTING'] = True
        appy.config['WTF_CSRF_ENABLED'] = False
        return appy

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def setUp(self):
        manage.inittestdb()
      #  print self.addShare("GOOG", 10, 100, "testportfolio").data

    def tearDown(self):

        db.session.remove()
        db.drop_all()
        manage.initdb()

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def addPortfolio(self, portfolioname):
        return self.client.post('/addportfolio', data=dict(
            name=portfolioname
        ), follow_redirects=True)

    def addShare(self, ticker, quantity, purchaseprice, portfolioid):
        #self.addPortfolio(portfolioid)
        return self.client.post('/add', data=dict(
            ticker=ticker,
            quantity=quantity,
            purchaseprice=purchaseprice,
            portfolioid=portfolioid
        ), follow_redirects=True)

    def testAddShare(self):
        self.login('lucas2', 'test')

        self.addPortfolio("testportfolio")
        rv = self.addShare("GOOG", 10, 100, "testportfolio")
        assert "Added share &#39;GOOG&#39;" in rv.data

        rv = self.addShare("GOOG", 10, 100, "testportfolio")
        assert "That share is already in that portfolio" in rv.data

        self.addPortfolio("secondtestportfolio")
        rv = self.addShare("GOOG", 10, 100, "secondtestportfolio")
        assert "Added share &#39;GOOG&#39;" in rv.data
