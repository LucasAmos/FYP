from datetime import datetime

from sqlalchemy import desc, ForeignKeyConstraint
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from thermos import db


# userownedshares = db.Table('user_owned_share',
#                            db.Column('share_ticker', db.String, db.ForeignKey('share.ticker')),
#                            db.Column('user_username', db.String, db.ForeignKey('user.username'))
#                            )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String)
    phonenumber = db.Column(db.String(15))
    emailupdate = db.Column(db.Boolean)
    updatefrequency = db.Column(db.Integer)
    #shares = db.relationship('Share', secondary=Userownedshare, backref=db.backref('User', lazy='dynamic'))
    shares = db.relationship('Userownedshare', backref='author', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return "<user '{}'>".format(self.username)


class Userownedshare(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        ticker = db.Column(db.String(20), db.ForeignKey('share.ticker'))
       # name = db.Column(db.String(50), nullable=False)
        share_owner = db.Column(db.String, db.ForeignKey('user.username'))
        namematch = db.relationship('Share', backref='userownedshare', foreign_keys=[ticker])
        ForeignKeyConstraint(['share_owner', 'ticker'], ['user.username', 'share.ticker'])


        def __repr__(self):
            return "*Userownedshare* " + " Ticker: " + self.ticker + " " + " Share owner: " + self.share_owner

class Share(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False)
        ticker = db.Column(db.String(50), db.ForeignKey('userownedshare.ticker'))
        tickermatch = db.relationship('Userownedshare', backref='share',  foreign_keys=[ticker])

        def __repr__(self):
            return "*Share*" + self.name + " " + " Ticker: " + self.ticker






# class Share(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     ticker = db.Column(db.String(20),)
#     name = db.Column(db.String(50), nullable=False, unique=True)
#     usershares = db.relationship('User', secondary=userownedshare, backref=db.backref('Share', lazy='dynamic'))
#
#
#
#     def __repr__(self):
#         return self.name

