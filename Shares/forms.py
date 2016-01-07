from flask_wtf import Form
from wtforms.fields import StringField, IntegerField, PasswordField, BooleanField, SubmitField
from flask.ext.wtf.html5 import DecimalField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, url, ValidationError
from flask_login import current_user
from models import User, Userownedshare


class ShareForm(Form):
    ticker = StringField('The share ticker:', validators=[DataRequired(), Regexp(r'^[a-zA-Z]*$',
                                                  message="The share ticker must only be letters")])
    quantity = IntegerField('How many of this share do you own:')
    dividends = DecimalField('Have you received any dividends for this share?')


    def validate_ticker(self, ticker_field):
        if Userownedshare.query.filter_by(ticker=ticker_field.data).filter_by(user=current_user.username).first():
            raise ValidationError('This share is already in your portfolio')


    def validate(self):

        if not Form.validate(self):
            return False

        return True

class EditShareForm(Form):
    ticker = StringField('The share ticker:', validators=[DataRequired(), Regexp(r'^[a-zA-Z]*$',
                                                  message="The share ticker must only be letters")])
    quantity = IntegerField('How many of this share do you own:')
    dividends = DecimalField('Have you received any dividends for this share?')


    def validate_ticker(self, ticker_field):
        print Userownedshare.query.filter_by(ticker=ticker_field.data).filter_by(user=current_user.username).count()
        if Userownedshare.query.filter_by(ticker=ticker_field.data).filter_by(user=current_user.username).count() != 1:
            raise ValidationError('You cannot edit a different share')


    def validate(self):

        if not Form.validate(self):
            return False

        return True


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





