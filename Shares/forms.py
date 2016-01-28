from flask_wtf import Form
from wtforms.fields import StringField, IntegerField, PasswordField, BooleanField, SubmitField, SelectField
from flask.ext.wtf.html5 import DecimalField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, url, ValidationError
from wtforms_components import read_only
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_admin.form.widgets import Select2Widget

from flask_login import current_user
from models import User, Userownedshare


class ExistingShareInPortfolioValidator(object):
    def __init__(self, message=None):
        if not message:
            message = u"That share is already in that portfolio"
        self.message = message

    def __call__(self, form, field):
        print form.data['ticker']
        print form.data['portfolioid']

        ticker = form.data['ticker']
        portfolioid = form.data['portfolioid']

        if Userownedshare.query.filter_by(ticker=ticker).filter_by(user=current_user.username).filter_by(portfolioid=portfolioid).first():
            raise ValidationError(self.message)


class AddShareForm(Form):
    ticker = StringField('The share ticker:', validators=[DataRequired(), Regexp(r'^[a-zA-Z]*$',
                                                                                 message="The share ticker must only be letters")])
    quantity = IntegerField('How many of this share do you own:')
    dividends = DecimalField('Do you have any dividends for this share? &nbsp')
    #portfolioid = StringField('Enter a portfolio name:', validators=[ExistingShareInPortfolioValidator()])
    portfolioid = SelectField(u'Or choose an existing portfolio:', validators=[ExistingShareInPortfolioValidator()])

    def validate(self):

        if not Form.validate(self):
            return False

        return True


class EditShareForm(Form):
    ticker = StringField('The share ticker:', validators=[DataRequired(), Regexp(r'^[a-zA-Z]*$',
                                                                                 message="The share ticker must only be letters")])
    quantity = IntegerField('How many of this share do you own:')
    dividends = DecimalField('Have you received any dividends for this share?')
    portfolioid = StringField('Enter a portfolio name')

    def validate(self):

        if not Form.validate(self):
            return False

        return True

    def __init__(self, *args, **kwargs):
        super(EditShareForm, self).__init__(*args, **kwargs)
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





