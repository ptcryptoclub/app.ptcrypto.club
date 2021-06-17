from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from ptCryptoClub.admin.models import User
from ptCryptoClub.admin.gen_functions import email_validation_disposable_emails


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

    def validate_new_pin(self, new_pin):
        to_validate = new_pin.data
        if not to_validate.isdigit():
            raise ValidationError('Your pin must be only digits.')
