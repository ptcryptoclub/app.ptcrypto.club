from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from wtforms.fields.html5 import DateField
from ptCryptoClub.admin.models import User
from ptCryptoClub.admin.gen_functions import email_validation_disposable_emails
import string
from datetime import datetime, date


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Length(max=255)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already in use!')

    def validate_email(self, email):
        control, message = email_validation_disposable_emails(email=email.data)
        if not control:
            raise ValidationError(message)
        email_control = User.query.filter_by(email=email.data).first()
        if email_control:
            raise ValidationError('Email already in use!')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    pin = StringField('Pin', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Login')


class AuthorizationForm(FlaskForm):
    pin = StringField('Pin', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Confirm MFA')
    submit_2 = SubmitField('Update')
    submit_3 = SubmitField('Delete my account')
    submit_4 = SubmitField('Submit competition')


class UpdateDetailsForm(FlaskForm):
    username = StringField('Username', validators=[Length(max=20)])
    email = StringField('Email', validators=[Length(max=255)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already in use!')

    def validate_email(self, email):
        control, message = email_validation_disposable_emails(email=email.data)
        if not control:
            raise ValidationError(message)
        email_control = User.query.filter_by(email=email.data).first()
        if email_control:
            raise ValidationError('Email already in use!')


class BuyAssetForm(FlaskForm):
    base = SelectField('base', validators=[DataRequired()])
    quote = SelectField('quote', validators=[DataRequired()])
    market = SelectField('market', validators=[DataRequired()])
    amount_spent = StringField('Amount', validators=[DataRequired()])
    submit = SubmitField('Buy asset')


class SellAssetForm(FlaskForm):
    base_sell = SelectField('base', validators=[DataRequired()])
    quote_sell = SelectField('quote', validators=[DataRequired()])
    market_sell = SelectField('market', validators=[DataRequired()])
    amount_spent_sell = StringField('Amount', validators=[DataRequired()])
    submit_sell = SubmitField('Sell asset')


class PasswordRecoveryEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Verify')


class PasswordRecoveryUsernameForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Verify')


class PasswordRecoveryConfirmationForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password'), Length(min=8)])
    submit = SubmitField('Reset password')


class FirstPinLogin(FlaskForm):
    new_pin = StringField('PIN', validators=[DataRequired(), Length(max=6, min=6)])
    new_pin_confirmation = StringField('Re-PIN', validators=[DataRequired(), Length(max=6, min=6), EqualTo('new_pin')])
    submit = SubmitField('Change PIN')

    def validate_new_pin(self, new_pin):
        to_validate = new_pin.data
        if not to_validate.isdigit():
            raise ValidationError('Your pin must be only digits.')


class CreateCompetitionForm(FlaskForm):
    name = StringField('Competition name', validators=[DataRequired(), Length(max=30)])
    start_date = DateField('Start date', validators=[DataRequired()])
    end_date = DateField('End date', validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])
    quote = SelectField('Quote', choices=[("eur", "EUR"), ("usd", "USD")], validators=[DataRequired()])
    buy_fee = StringField('Buy fee (%)', validators=[DataRequired()])
    sell_fee = StringField('Sell fee (%)', validators=[DataRequired()])
    max_users = StringField('Users limit')
    users = SelectField('Users type', choices=[(0, "All")], validators=[DataRequired()])
    p_email = BooleanField('Promotional email')
    submit = SubmitField('Create competition')
    submit_2 = SubmitField('Modify competition')

    def validate_name(self, name):
        if not name.data[0] in string.ascii_letters:
            raise ValidationError('Must start with a letter')

    def validate_amount(self, amount):
        if not amount.data.isdigit():
            raise ValidationError('Must be a positive integer')

    def validate_buy_fee(self, buy_fee):
        try:
            fee = float(buy_fee.data)
        except Exception as e:
            print(e)
            raise ValidationError('Must be a decimal between 0 and 1')
        else:
            if fee >= 100:
                raise ValidationError('Cannot be >= 1')
            elif fee < 0:
                raise ValidationError('Cannot be negative')

    def validate_sell_fee(self, sell_fee):
        try:
            fee = float(sell_fee.data)
        except Exception as e:
            print(e)
            raise ValidationError('Must be a decimal between 0 and 1')
        else:
            if fee >= 100:
                raise ValidationError('Cannot be >= 1')
            elif fee < 0:
                raise ValidationError('Cannot be negative')

    def validate_max_users(self, max_users):
        if max_users.data == "":
            pass
        elif not max_users.data.isdigit():
            raise ValidationError('Must be a positive integer')

    def validate_start_date(self, start_date):
        date_now = datetime.utcnow()
        if start_date.data < date(date_now.year, date_now.month, date_now.day):
            raise ValidationError("Start date cannot be in the past")
        elif self.end_date.data == start_date.data:
            raise ValidationError("Start and end date cannot be the same")
        elif start_date.data == date(date_now.year, date_now.month, date_now.day):
            raise ValidationError("Start date cannot be today")
        elif start_date.data > self.end_date.data:
            raise ValidationError("Start date cannot be after end date")

    def validate_end_date(self, end_date):
        date_now = datetime.utcnow()
        if end_date.data < date(date_now.year, date_now.month, date_now.day):
            raise ValidationError("End date cannot be in the past")
        elif self.start_date.data == end_date.data:
            raise ValidationError("Start and end date cannot be the same")
        elif end_date.data == date(date_now.year, date_now.month, date_now.day):
            raise ValidationError("End date cannot be today")
        elif end_date.data < self.start_date.data:
            raise ValidationError("End date cannot be before start date")


class BuyAssetFormCompetition(FlaskForm):
    base = SelectField('base', validators=[DataRequired()])
    quote = SelectField('quote', choices=[("eur", "EUR")], validators=[DataRequired()])
    market = SelectField('market', choices=[("kraken", "kraken")], validators=[DataRequired()])
    amount_spent = StringField('Amount', validators=[DataRequired()])
    submit = SubmitField('Buy asset')


class SellAssetFormCompetition(FlaskForm):
    base_sell = SelectField('base', validators=[DataRequired()])
    quote_sell = SelectField('quote', choices=[("eur", "EUR")], validators=[DataRequired()])
    market_sell = SelectField('market', choices=[("kraken", "kraken")], validators=[DataRequired()])
    amount_spent_sell = StringField('Amount', validators=[DataRequired()])
    submit_sell = SubmitField('Sell asset')
