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

    def tearDown(self):

        db.session.remove()
        db.drop_all()


    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.post('/logout', follow_redirects=True)

    def test_login(self):

        rv = self.login('lucas2', 'test')
        assert 'Welcome Lucas2' in rv.data

        rv = self.login('nouser', 'test')
        assert 'Incorrect username or password' in rv.data

        rv = self.login('lucas', 'wrongpassword')
        assert 'Incorrect username or password' in rv.data

        rv = self.logout()
        assert 'Sign in' in rv.data



    def addPortfolio(self, portfolioname):
        self.login('test', 'test')
        return self.client.post('/addportfolio', data=dict(
            name=portfolioname
        ), follow_redirects=True)

    def test_addPortfolio(self):
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
        rv = self.addPortfolio("testportfolioname")
        assert "testportfolioname" in rv.data

        # rv=self.deletePortfolio("testportfolioname")
        # assert "deleted portfolio 'testportfolioname'" in rv.data
