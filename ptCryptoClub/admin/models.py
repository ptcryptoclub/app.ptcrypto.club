from ptCryptoClub import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    account_type = db.Column(db.Integer, nullable=False, default=1)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    hash = db.Column(db.String(255), nullable=False)
    active_qr = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=False)
    date_active = db.Column(db.DateTime)
    qrcode_secret = db.Column(db.String(255), nullable=False)
    qrcode_img = db.Column(db.String(255), unique=True)
    api_secret = db.Column(db.String(255), nullable=False)


class LoginUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_ID = db.Column(db.Integer)
    username = db.Column(db.String(255))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ipAddress = db.Column(db.String(255))
    status = db.Column(db.Boolean)


class ErrorLogs(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(255), nullable=False)
    log = db.Column(db.Text)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class UpdateAuthorizationDetails(db.Model, UserMixin):
    pin_id = db.Column(db.Integer, primary_key=True)
    pin_hash = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    old_username = db.Column(db.String(255))
    old_email = db.Column(db.String(255))
    new_username = db.Column(db.String(255))
    new_email = db.Column(db.String(255))
    valid = db.Column(db.Boolean, nullable=False, default=True)
    used = db.Column(db.Boolean, nullable=False, default=False)


class TransactionsPTCC(db.Model, UserMixin):
    trans_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    market = db.Column(db.String(255), nullable=False)
    base = db.Column(db.String(255), nullable=False)
    quote = db.Column(db.String(255), nullable=False)
    asset_amount = db.Column(db.Float, nullable=False)
    asset_price = db.Column(db.Float, nullable=False)
    value = db.Column(db.Float, nullable=False)
    fee = db.Column(db.Float, nullable=False)
