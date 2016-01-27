#! /usr/bin/env python

from Shares import app, db

from Shares.models import User, Userownedshare, Share
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

        lucas=User(username="lucas", email="lucas@example.com", password="test")
        db.session.add(lucas)

        share = Share(ticker="GOOG", name="ALPHABET inc")
        db.session.add(share)

        goog = Userownedshare(user="lucas", ticker="GOOG", quantity=1, portfolioid="test portfolio")
        db.session.add(goog)
        #
        # apple2 = Userownedshare(user="reindert", ticker="AAPL", quantity=1)
        # db.session.add(apple2)
        #
        # ibm = Userownedshare(user="lucas", ticker="IBM", quantity=1)
        # db.session.add(ibm)
        #

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
def dropdb():
    if prompt_bool(
        "Are you sure you want to lose all your data?"):
        db.drop_all()
        print('Dropped the database')

if __name__ == '__main__':
    manager.run()
