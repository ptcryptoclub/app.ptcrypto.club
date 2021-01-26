# external imports
from flask import render_template, url_for, flash, redirect, request, session, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, timedelta
import random
import pyotp
import os
import werkzeug

# local imports
from ptCryptoClub import app, db, bcrypt
from ptCryptoClub.admin.config import admins_emails, default_delta, default_latest_transactions, default_last_x_hours, default_datapoints, \
                                        candle_options, default_candle, QRCode, TRANSACTION_SUCCESS_STATUSES
from ptCryptoClub.admin.models import User
from ptCryptoClub.admin.gen_functions import get_all_markets, get_all_pairs, card_generic, table_latest_transactions
from ptCryptoClub.admin.sql.ohlc_functions import line_chart_data, ohlc_chart_data
from ptCryptoClub.admin.forms import RegistrationForm, LoginForm, AuthorizationForm
from ptCryptoClub.admin.auto_email import Email


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
        "all_markets": get_all_markets(),
        "default_candle": default_candle
    }


@app.route("/")
def home():
    cards = []
    markets = get_all_markets()
    for market in markets:
        for pair in get_all_pairs(market):
            dict_ = card_generic(base=pair['base'], quote=pair['quote'], market=pair['market'], delta=default_delta)
            cards.append(dict_)
    tables = []
    number_of_trans = default_latest_transactions
    for market in markets:
        for pair in get_all_pairs(market):
            tables.append(
                table_latest_transactions(base=pair['base'], quote=pair['quote'], market=pair['market'], number_of_trans=number_of_trans)
            )
    return render_template(
        "index.html",
        title="Home",
        cards=cards,
        tables=tables,
        number_of_trans=number_of_trans
    )


@app.route("/api/home/cards/<base>/<quote>/<market>/<delta>/")
def api_home_cards(base, quote, market, delta):
    return jsonify(
        card_generic(base=base, quote=quote, market=market, delta=delta)
    )


@app.route("/api/home/latest-transactions/<base>/<quote>/<market>/<number_of_trans>/")
def api_home_latest_transactions(base, quote, market, number_of_trans):
    return jsonify(
        table_latest_transactions(base=base, quote=quote, market=market, number_of_trans=number_of_trans)
    )


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit() and request.method == "POST":
        username = form.username.data
        password = form.password.data
        given_code = form.pin.data
        user = User.query.filter_by(username=username).first()
        if user is not None:
            secret = user.qrcode_secret
            totp = pyotp.TOTP(secret)
            if not user.active_qr:
                flash(f'Please set up MFA to complete your registration process.', 'info')
                return redirect(url_for('qr_activation', ID=user.qrcode_img))
            elif not user.active:
                flash(f'Your account has not been activated yet, please check your email.', 'info')
                return redirect(url_for('home'))
            elif bcrypt.check_password_hash(user.password, password) and totp.verify(given_code):
                login_user(user, remember=False)
                flash(f'You are now logged in', 'success')
                return redirect(url_for('home'))
            else:
                flash(f'Incorrect login details, please try again.', 'danger')
                return render_template(
                    "login.html",
                    title="Login",
                    form=form
                )
        else:
            flash(f'Incorrect username or password, please try again.', 'danger')
            return render_template(
                "login.html",
                title="Login",
                form=form
            )
    else:
        return render_template(
            "login.html",
            title="Login",
            form=form
        )


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/register/", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit() and request.method == "POST":
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        hash = bcrypt.generate_password_hash(form.email.data + str(random.getrandbits(64))).decode('utf-8')
        api_secret = str(random.getrandbits(random.randint(128, 256)))
        qrcode_secret = pyotp.random_base32()
        url = pyotp.totp.TOTP(qrcode_secret).provisioning_uri(name=form.username.data, issuer_name='app.ptcrypto.club')
        filename = str(random.getrandbits(64))
        QRCode(info=url, filename=filename)
        # noinspection PyArgumentList
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            hash=hash,
            qrcode_secret=qrcode_secret,
            api_secret=api_secret,
            qrcode_img=filename
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('qr_activation', ID=filename))
    else:
        return render_template(
            'register.html',
            title="Register",
            form=form
        )


@app.route("/mfa/<ID>/", methods=["GET", "POST"])
def qr_activation(ID):
    form = AuthorizationForm()
    user = User.query.filter_by(qrcode_img=ID).first()
    if user is None:
        return redirect(url_for('home'))
    if user.active_qr:
        flash(f'You already activated MFA in your account.', 'info')
        return redirect(url_for('home'))
    secret = user.qrcode_secret
    if form.validate_on_submit() and request.method == "POST":
        totp = pyotp.TOTP(secret)
        given_code = form.pin.data
        if totp.verify(given_code):
            os.remove(f'/home/heldercepeda/PycharmProjects/production/appPtCryptoClub/ptCryptoClub/static/qrcodes/{user.qrcode_img}.png')
            user.active_qr = True
            # Email().send_email(email=form.email.data, hash=hash)
            user.qrcode_img = None
            db.session.commit()
            flash(f'Your account has been create. Please check your email to activate your account.', 'success')
            return redirect(url_for('market', market="kraken"))
        else:
            flash(f'The passcode you provided is not correct. Please try again.', 'danger')
            return render_template(
                'qrcodeactivation.html',
                title="QRCode",
                form=form,
                qrcode_img=f'{user.qrcode_img}.png'
            )
    else:
        return render_template(
            'qrcodeactivation.html',
            title="QRCode",
            form=form,
            qrcode_img=f'{user.qrcode_img}.png'
        )


@app.route('/activate-account')
def activate_account():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        hash = request.args.get('hash')
        email = request.args.get('email')
        if hash and email:
            user = User.query.filter_by(email=email, hash=hash).first()
            if user:
                if user.active:
                    flash("Your account is already active.", "info")
                    return redirect(url_for('home'))
                else:
                    user.active = True
                    if user.date_active is None:
                        user.date_active = datetime.utcnow()
                    db.session.commit()
                    flash(f'Your account has been activated.', 'success')
                    return redirect(url_for('login'))
            else:
                flash(f'Your activation details are incorrect, please try again.', 'danger')
                return redirect(url_for('home'))
        else:
            flash(f'Your activation details are incorrect, please try again.', 'danger')
            return redirect(url_for('home'))


@app.route("/market/<market>/")
def market(market):
    cards = []
    for pair in get_all_pairs(market):
        dict_ = card_generic(base=pair['base'], quote=pair['quote'], market=pair['market'], delta=default_delta)
        cards.append(dict_)
    return render_template(
        "market.html",
        title="Markets",
        market=market,
        cards=cards,
        num_pairs=len(cards)
    )


@app.route("/charts/line/<market>/<base>/<quote>/")
def chart_line(market, base, quote):
    return render_template(
        "charts-line.html",
        title="Charts",
        market=market,
        base=base,
        quote=quote,
        delta=default_delta,
        last_x_hours=default_last_x_hours
    )


@app.route("/api/line-chart/info/<market>/<base>/<quote>/<delta>/")
def api_charts_line_info(market, base, quote, delta):
    return jsonify(
        card_generic(base, quote, market, delta)
    )


@app.route("/api/charts/line/<market>/<base>/<quote>/<last_x_hours>/")
def api_charts_line_data(market, base, quote, last_x_hours):
    return jsonify(
        line_chart_data(base, quote, market, last_x_hours)
    )


@app.route("/charts/ohlc/<market>/<base>/<quote>/<candle>")
def chart_ohlc(market, base, quote, candle):
    try:
        candle = int(candle)
    except Exception as e:
        print(e)
        candle = 60
    if candle == 20:
        candle_in_use_display = "20 sec"
    elif candle == 60:
        candle_in_use_display = "1 min"
    elif candle == 300:
        candle_in_use_display = "5 min"
    else:
        return redirect(url_for('chart_ohlc', market='kraken', base='btc', quote='eur', candle=default_candle))
    return render_template(
        "charts-ohlc.html",
        title="Charts",
        market=market,
        base=base,
        quote=quote,
        datapoints=default_datapoints,
        candles=candle_options,
        candle_in_use=candle,
        candle_in_use_display=candle_in_use_display
    )


@app.route("/api/charts/ohlc/<market>/<base>/<quote>/<datapoints>/<candle>/")
def api_charts_ohlc_data(market, base, quote, datapoints, candle):
    return jsonify(
        ohlc_chart_data(base, quote, market, datapoints, candle)
    )
