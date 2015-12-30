#! /usr/bin/env python

from thermos import app, db

from thermos.models import User, Userownedshare, Share
from flask.ext.script import Manager, prompt_bool
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def initdb():
        db.create_all()
        reindert=User(username="reindert", email="reindert@example.com", password="test")
        db.session.add(reindert)

        lucas=User(username="lucas", email="lucas@example.com", password="test")
        db.session.add(lucas)


        google = Userownedshare(user="reindert", ticker="GOOG", quantity=1)
        db.session.add(google)

        apple = Userownedshare(user="lucas", ticker="AAPL", quantity=1)
        db.session.add(apple)

        apple2 = Userownedshare(user="reindert", ticker="AAPL", quantity=1)
        db.session.add(apple2)

        ibm = Userownedshare(user="lucas", ticker="IBM", quantity=1)
        db.session.add(ibm)

        share = Share(ticker="GOOG", name="ALPHABET inc")
        db.session.add(share)

        share2 = Share(ticker="AAPL", name="APPLE inc")
        db.session.add(share2)

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
