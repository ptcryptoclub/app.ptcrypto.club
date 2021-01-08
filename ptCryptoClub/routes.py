# external imports
from flask import render_template, url_for, flash, redirect, request, session, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, timedelta
import random
import werkzeug

# local imports
from ptCryptoClub import app, db, bcrypt
from ptCryptoClub.admin.config import admins_emails, TRANSACTION_SUCCESS_STATUSES
from ptCryptoClub.admin.models import User
from ptCryptoClub.admin.gen_functions import get_all_markets, get_all_pairs, card_generic


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=15)


@app.template_filter()
def numberFormat(value):
    return f"{value : ,}"


@app.context_processor
def send_my_func():
    return {
        "admins_emails": admins_emails,
        "all_markets": get_all_markets()
    }


@app.route("/")
def home():
    cards = []
    for market in get_all_markets():
        for pair in get_all_pairs(market):
            dict_ = card_generic(base=pair['base'], quote=pair['quote'], market=pair['market'], delta=60*24)
            cards.append(dict_)
    tables = []
    return render_template(
        "index.html",
        title="Home",
        cards=cards,
        tables=tables
    )


@app.route("/market/<market>")
def market(market):
    cards = []
    for pair in get_all_pairs(market):
        dict_ = card_generic(base=pair['base'], quote=pair['quote'], market=pair['market'], delta=60 * 24)
        cards.append(dict_)
    return render_template(
        "market.html",
        title="Markets",
        market=market,
        cards=cards
    )
