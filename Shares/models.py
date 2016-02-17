from datetime import datetime

from sqlalchemy import desc
from flask_login import UserMixin, current_user
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
    shares = db.relationship('Userownedshare', backref='Userownedshare', lazy='dynamic')

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
        user = db.Column(db.String, db.ForeignKey('user.username'))
        quantity = db.Column(db.Integer, nullable=False)
        dividends = db.Column(db.Float, server_default="0.0")
        triggerlevel = db.Column(db.Integer)
        smsalert = db.Column(db.Boolean)
        emailalert = db.Column(db.Boolean)
        portfolioid = db.Column(db.String(50))
        averagepurchaseprice = db.Column(db.Float, server_default="0.0")
        name = db.relationship('Share', backref='userownedshare',  foreign_keys=[ticker], lazy="joined")
        owner = db.relationship('User', backref='userownedshare',  foreign_keys=[user], lazy="joined")


        @staticmethod
        def all(username):
            return Userownedshare.query.filter_by(user=username).all()

        @staticmethod
        def listshares():

            if current_user.is_authenticated:

              return Userownedshare.query.order_by(desc(Userownedshare.ticker)).filter_by(user=current_user.username)

        def __repr__(self):
            return "**Userownedshare** " + " Ticker: " + self.ticker + " " + " Share owner: " + self.user



# is this being user anywhere? yes!
        @staticmethod
        def listportfolios(user):

                shares = Userownedshare.query.order_by(desc(Userownedshare.ticker)).filter_by(user=user).filter(Userownedshare.portfolioid != "")

                tempset = set()
                for row in shares:
                    id = row.portfolioid
                    tempset.add(id)

                templist = list(tempset)

                return templist


class Share(db.Model):
        id = db.Column(db.Integer)
        name = db.Column(db.String(50), nullable=False)
        ticker = db.Column(db.String(50), primary_key=True)
        tickermatch = db.relationship('Userownedshare', backref='share', cascade="all, delete-orphan", lazy="joined")
        @staticmethod
        def exists(shareticker):

            if Share.query.filter_by(ticker=shareticker).first():
                return True
            else:
                return False

        def __repr__(self):
            return "*Share* " + self.name + " " + " Ticker: " + self.ticker


class Portfolios(db.Model):
    portfolioname = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(50), primary_key=True)
