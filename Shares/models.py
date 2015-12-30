from datetime import datetime

from sqlalchemy import desc
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from Shares import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String)
    phonenumber = db.Column(db.String(15))
    emailupdate = db.Column(db.Boolean)
    updatefrequency = db.Column(db.Integer)
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
        id = db.Column(db.Integer)
        ticker = db.Column(db.String(20), db.ForeignKey('share.ticker'), primary_key=True)
        user = db.Column(db.String, db.ForeignKey('user.username'), primary_key=True)
        quantity = db.Column(db.Integer, nullable=False)
        dividends = db.Column(db.Float)
        triggerlevel = db.Column(db.Integer)
        smsalert = db.Column(db.Boolean)
        emailalert = db.Column(db.Boolean)
        portfolioid = db.Column(db.String(50))
        name = db.relationship('Share', backref='userownedshare', foreign_keys=[ticker])

        def __repr__(self):
            return "*Userownedshare* " + " Ticker: " + self.ticker + " " + " Share owner: " + self.user

class Share(db.Model):
        id = db.Column(db.Integer)
        name = db.Column(db.String(50), nullable=False)
        ticker = db.Column(db.String(50), db.ForeignKey('userownedshare.ticker'), primary_key=True)
        tickermatch = db.relationship('Userownedshare', backref='share',  foreign_keys=[ticker])

        def __repr__(self):
            return "*Share* " + self.name + " " + " Ticker: " + self.ticker


