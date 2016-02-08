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
       #print self.addShare("GOOG", "ee", 100, "testportfolio").data
        print self.login("test", "test").data

    def tearDown(self):

        db.session.remove()
        db.drop_all()


    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)


    def test_login(self):
        lucas=User(username="lucas2", email="lucas2@example.com", password="test")
        db.session.add(lucas)

        rv = self.login('lucas2', 'test')
        assert 'Welcome' in rv.data

    def addPortfolio(self, portfolioname):
        self.login('test', 'test')
        return self.client.post('/addportfolio', data=dict(
            name=portfolioname
        ), follow_redirects=True)

    def test_addPortfolio(self):

        rv = self.login("test", "test")

        rv = self.addPortfolio("testportfolioname")

        assert "testportfolioname" in rv.data
        assert "notavalidname" not in rv.data




    def addShare(self, ticker, quantity, purchaseprice, portfolioid):
        self.login("test", "test")
        self.addPortfolio("testportfolio")
        return self.client.post('/add', data=dict(
            ticker=ticker,
            quantity=quantity,
            purchaseprice=purchaseprice,
            portfolioid=portfolioid
        ), follow_redirects=True)

    def testAddShare(self):
        rv = self.addShare("GOOG", 10, 100, "testportfolio")
        assert "Added share" in rv.data
        assert "GOOG" in rv.data


    def deletePortfolio(self, portfolioname):
        self.login("test", "test")
        return self.client.post('/deleteportfolio', data=dict(
            name2=portfolioname
        ), follow_redirects=True)

    def testDeletePortfolio(self):
        self.addPortfolio("testportfolioname")
        rv = self.login("test", "test")
        assert "testportfolioname" in rv.data

