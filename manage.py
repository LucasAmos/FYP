#test
#! /usr/bin/env python

from Shares import app, db

from Shares.models import User, Userownedshare, Share, Portfolios, Transactions
from flask.ext.script import Manager, prompt_bool
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand



manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def initdb():
        db.create_all()
        # reindert=User(username="reindert", email="reindert@example.com", password="test")
        # db.session.add(reindert)

        lucas=User(username="lucas", email="xkv1922c@gmail.com", password="test", emailfrequency=0, smsenabled=False, phonenumber="07506292708")
        db.session.add(lucas)

        portfolio = Portfolios(username="lucas", portfolioname="test")
        db.session.add(portfolio)

        #transaction = Transaction(user="lucas", portfolioid="test", buySell="sell", quantity=6, dividends=476.44, price= 324.3, ticker="RBS")

        #transaction = Transaction(id=1)
        #db.session.add(transaction)




        google = Userownedshare(user="lucas", ticker="MKS", quantity=1, portfolioid="test", triggerlevel=0, smsalert=False, emailalert=False)
        db.session.add(google)
        #
        # apple2 = Userownedshare(user="reindert", ticker="AAPL", quantity=1)
        # db.session.add(apple2)
        #
        # ibm = Userownedshare(user="lucas", ticker="IBM", quantity=1)
        # db.session.add(ibm)
        #
        share = Share(ticker="MKS", name="Marks & Spencer")
        db.session.add(share)
        #
        # share2 = Share(ticker="AAPL", name="APPLE inc")
        # db.session.add(share2)
        #
        # share3 = Share(ticker="IBM", name="INTERNATIONAL BUSINESS MACHINES")
        # db.session.add(share3)
        #
        # XOM = Share(ticker="XOM", name="EXXON MOBIL CORPORATION")
        # db.session.add(XOM)
        #
        # db.session.commit()

        # lucas=User(username="lucas", email="lucas@example.com", password="test")
        # db.session.add(lucas)
        db.session.commit()


        print('Database initialised')


@manager.command
def inittestdb():
        db.create_all()
        testuser=User(username="test", email="test@test.com", password="test")
        db.session.add(testuser)
        lucas=User(username="lucas2", email="lucas2@example.com", password="test")
        db.session.add(lucas)
        portfolio=Portfolios(portfolioname="Portfolio1", username="test")
        db.session.add(portfolio)


@manager.command
def dropdb():
    if prompt_bool(
        "Are you sure you want to lose all your data?"):
        db.drop_all()
        print('Dropped the database')

if __name__ == '__main__':
    manager.run()
