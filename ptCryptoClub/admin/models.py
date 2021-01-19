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
    active = db.Column(db.Boolean, default=False)
    date_active = db.Column(db.DateTime)
    qrcode_secret = db.Column(db.String(255), nullable=False)
    api_secret = db.Column(db.String(255), nullable=False)


class LoginUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_ID = db.Column(db.Integer)
    username = db.Column(db.String(255))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ipAddress = db.Column(db.String(255))
    status = db.Column(db.Boolean)
    cookie = db.Column(db.Text)
    raw = db.Column(db.Text)


class ErrorLogs(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(255), nullable=False)
    log = db.Column(db.Text)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class LivePairs(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    base = db.Column(db.String(255), nullable=False)
    quote = db.Column(db.String(255), nullable=False)
    market = db.Column(db.String(255), nullable=False)
    price_rate = db.Column(db.Integer, nullable=False)
    trade_rate = db.Column(db.Integer, nullable=False)
    ohlc_periods = db.Column(db.Integer, nullable=False)
    order_book_rate = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, nullable=False)
    in_use = db.Column(db.Boolean, nullable=False)
    added_by = db.Column(db.Integer, nullable=False)

