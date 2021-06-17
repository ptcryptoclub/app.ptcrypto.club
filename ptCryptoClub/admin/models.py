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


class MFA(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    mfa = db.Column(db.Boolean, nullable=False, default=False)
    r_pin = db.Column(db.String(60), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    first_login = db.Column(db.Boolean)


class MFARequests(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    hash = db.Column(db.String(255), nullable=False)
    valid = db.Column(db.Boolean, nullable=False, default=True)
    used = db.Column(db.Boolean, nullable=False, default=False)
    deactivate = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Reset2FARequests(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    hash_1 = db.Column(db.String(255), nullable=False)
    hash_2 = db.Column(db.String(255), nullable=False)
    valid = db.Column(db.Boolean, nullable=False, default=True)
    used = db.Column(db.Boolean, nullable=False, default=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class ApiUsage(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime)
    usage = db.Column(db.BigInteger, nullable=False, default=0)


class IpAddressLog(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(255))
    date = db.Column(db.DateTime)


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


class Portfolio(db.Model, UserMixin):
    portfolio_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    start = db.Column(db.Integer, default=10_000)
    wallet = db.Column(db.Float, default=10_000)


class PortfolioAssets(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    asset = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, default=0)


class PortfolioRecord(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    value = db.Column(db.Float)
    wallet = db.Column(db.Float)
    assets = db.Column(db.Float)
    percentage = db.Column(db.Float)
    quote = db.Column(db.String(255), default="eur")


class ResetPasswordAuthorizations(db.Model, UserMixin):
    auth_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    hash = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    valid = db.Column(db.Boolean, nullable=False, default=True)
    used = db.Column(db.Boolean, nullable=False, default=False)
