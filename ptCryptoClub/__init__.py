from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS

from ptCryptoClub.admin.config import GenConfig


app = Flask(__name__)
app.config['SECRET_KEY'] = GenConfig.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = GenConfig.prod_db
app.config['BT_ENVIRONMENT'] = GenConfig.BT_ENVIRONMENT
app.config['BT_MERCHANT_ID'] = GenConfig.BT_MERCHANT_ID
app.config['BT_PUBLIC_KEY'] = GenConfig.BT_PUBLIC_KEY
app.config['BT_PRIVATE_KEY'] = GenConfig.BT_PRIVATE_KEY
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
cors = CORS(
    app,
    resources={
        r"/api/*": {"origins": [
            "https://ptcrypto.club",
            "https://iam.ptcrypto.club"
        ]}
    }
)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "info"
login_manager.session_protection = 'strong'
login_manager.refresh_view = 'login'
login_manager.needs_refresh_message = u"Session timed out, please re-login"
login_manager.needs_refresh_message_category = "info"

from ptCryptoClub import routes
