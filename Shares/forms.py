from flask_wtf import Form
from wtforms.fields import StringField, IntegerField, PasswordField, BooleanField, SubmitField, SelectField, HiddenField, FloatField
from flask.ext.wtf.html5 import DecimalField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, url, ValidationError, number_range, optional
from wtforms_components import read_only
from share_data import *

from flask_login import current_user
from models import *


class ExistingShareInPortfolioValidator(object):
    def __init__(self, message=None):
        if not message:
            message = u"That share is already in that portfolio"
        self.message = message

    def __call__(self, form, field):

        ticker = form.data['ticker']
        portfolioid = form.data['portfolioid']
        originalportfolioid = form.data['originalportfolioid']

        if Userownedshare.query.filter_by(ticker=ticker.upper()).filter_by(user=current_user.username).filter_by(portfolioid=portfolioid).first() and originalportfolioid != portfolioid:
            raise ValidationError(self.message)


class ExistingPortfolioValidator(object):
    def __init__(self, message=None):
        if not message:
            message = u"A portfolio with that name already exists"
        self.message = message

    def __call__(self, form, field):

        name = form.data['name'].lower()

        if Portfolios.query.filter_by(portfolioname=name).filter_by(username=current_user.username).first():
            raise ValidationError(self.message)

        if name == "":
            raise ValidationError("You must enter a portfolio name")


class EmptyPortfolioValidator(object):
    def __init__(self, message=None):
        if not message:
            message = u"You cannot delete portfolios that contain shares"
        self.message = message

    def __call__(self, form, field):

        name = form.data['name']

        if Userownedshare.query.filter_by(user=current_user.username).filter_by(portfolioid=name).first():
            raise ValidationError(self.message)


class SharePricevalidator(object):
    def __init__(self, message=None):
        if not message:
            message = u"Enter the share quantity purchased"
        self.message = message

    def __call__(self, form, field):

        if field.data and not form.data['sharequantity']:
            raise ValidationError(self.message)


class ShareQuantityValidator(object):
    def __init__(self, message=None):
        if not message:
            message = u"You must also enter the price paid for these shares"
        self.message = message

    def __call__(self, form, field):

        if field.data and not form.data['shareprice']:
            raise ValidationError(self.message)


class ShareTickerValidator(object):
    def __init__(self, message=None):
        if not message:
            message = u"No company exists for that symbol"
        self.message = message

    def __call__(self, form, field):

        symbol = form.data['ticker']

        if not share_data.isValidShare(symbol):
            raise ValidationError(self.message)



class AddShareForm(Form):
    ticker = StringField('The share ticker:', validators=[DataRequired(), Regexp(r'^[a-zA-Z]*$',
                                                                                 message="The share ticker must only be letters"), ShareTickerValidator()])
    quantity = IntegerField('How many of this share do you own:', validators=[optional(), number_range(min=1, max=10000)])
    dividends = DecimalField('Do you have any dividends for this share? &nbsp', validators=[optional(), number_range(min=0.00)])
    originalportfolioid = HiddenField("hidden field")
    purchaseprice = DecimalField('How much did you pay for each of these shares? &nbsp', validators=[optional(), number_range(min=0.0)])
    portfolioid = SelectField(u'Choose a portfolio:', validators=[ExistingShareInPortfolioValidator()])

    def validate(self):

        if not Form.validate(self):
            return False

        return True


class RemoveShareForm(Form):
    ticker = StringField('The share ticker:', validators=[DataRequired(), Regexp(r'^[a-zA-Z]*$',
                                                                                 message="The share ticker must only be letters")])
    quantity = IntegerField('How many of this share did you sell:', validators=[number_range(min=1, max=10000)])
    price = DecimalField('What price did you sell them for', validators=[optional(), number_range(min=0.00)])
    originalportfolioid = HiddenField("hidden field")
    portfolioid = SelectField('Choose a portfolio to add the share to:', validators=[ExistingShareInPortfolioValidator()])

    def validate(self):

        if not Form.validate(self):
            return False

        return True

    def __init__(self, *args, **kwargs):
        super(RemoveShareForm, self).__init__(*args, **kwargs)
        read_only(self.ticker)


class LoginForm(Form):
    username = StringField('Your Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class SignupForm(Form):
    username = StringField('Username',
                           validators=[
                               DataRequired(), Length(3, 80),
                               Regexp('^[A-Za-z0-9_]{3,}$',
                                      message='Usernames consist of numbers, letters and underscores')])

    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 120), Email()])

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('There is already a user with this email address.')

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken.')


class AddPortfolioForm(Form):
    name = StringField('New portfolio name: &nbsp ', validators=[ExistingPortfolioValidator(), Regexp(r'^[a-zA-Z0-9]*$',
                                                                                 message="The portfolio name must contain only letters and numbers")])

    def validate(self):

        if not Form.validate(self):
            return False

        return True


class AddAdditionalShares(Form):
    name = StringField('Share name')
    sharequantity = IntegerField('Have you bought any additional shares:', validators=[ShareQuantityValidator(), number_range(min=1, max=10000)])
    shareprice = FloatField('How much did you pay for these shares:', validators=[SharePricevalidator(), number_range(min=1, max=10000)])
    dividends = DecimalField('Have you received any new dividends: &nbsp', validators=[optional(), number_range(min=0.00)])

    def validate(self):

        if not Form.validate(self):
            return False

        return True

class DeletePortfolioForm(Form):
    name = SelectField('Select a portfolio to delete: &nbsp ', validators=[EmptyPortfolioValidator()])

    def validate(self):

        if not Form.validate(self):
            return False

        return True

