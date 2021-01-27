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
from ptCryptoClub.admin.models import User, LoginUser, UpdateAuthorizationDetails, ErrorLogs
from ptCryptoClub.admin.gen_functions import get_all_markets, get_all_pairs, card_generic, table_latest_transactions, hide_ip
from ptCryptoClub.admin.sql.ohlc_functions import line_chart_data, ohlc_chart_data
from ptCryptoClub.admin.forms import RegistrationForm, LoginForm, AuthorizationForm, UpdateDetailsForm
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
                # noinspection PyArgumentList
                log = LoginUser(user_ID=user.id,
                                ipAddress=request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
                                status=True)
                db.session.add(log)
                db.session.commit()
                return redirect(url_for('home'))
            else:
                # noinspection PyArgumentList
                log = LoginUser(user_ID=user.id,
                                ipAddress=request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
                                status=False)
                db.session.add(log)
                db.session.commit()
                flash(f'Incorrect login details, please try again.', 'danger')
                return render_template(
                    "login.html",
                    title="Login",
                    form=form
                )
        else:
            # noinspection PyArgumentList
            log = LoginUser(username=username,
                            ipAddress=request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
                            status=False)
            db.session.add(log)
            db.session.commit()
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
            Email().activation_email(email=user.email, hash=user.hash, username=user.username)
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


@app.route("/account/", methods=["GET", "POST"])
@login_required
def account_user():
    for update_request in UpdateAuthorizationDetails.query.filter_by(user_id=current_user.id, valid=True):
        update_request.valid = False
    db.session.commit()
    update_details_form = UpdateDetailsForm()
    if update_details_form.validate_on_submit():
        if update_details_form.username.data == '' and update_details_form.email.data == '':
            return redirect(url_for('account_user'))
        else:
            if update_details_form.username.data == '':
                # THIS WILL ONLY UPDATE THE EMAIL
                pin_hash = str(random.getrandbits(128))
                new_email = update_details_form.email.data
                print(new_email)
                # noinspection PyArgumentList
                update_request = UpdateAuthorizationDetails(
                    pin_hash=pin_hash,
                    user_id=current_user.id,
                    old_email=current_user.email,
                    new_email=new_email
                )
                db.session.add(update_request)
                db.session.commit()
                return redirect(url_for('mfa_authorization', user_id=current_user.id, pin_hash=pin_hash))
            elif update_details_form.email.data == '':
                # THIS WILL ONLY UPDATE THE USERNAME
                pin_hash = str(random.getrandbits(128))
                new_username = update_details_form.username.data
                print(new_username)
                # noinspection PyArgumentList
                update_request = UpdateAuthorizationDetails(
                    pin_hash=pin_hash,
                    user_id=current_user.id,
                    old_username=current_user.username,
                    new_username=new_username
                )
                db.session.add(update_request)
                db.session.commit()
                return redirect(url_for('mfa_authorization', user_id=current_user.id, pin_hash=pin_hash))
            else:
                # THIS WILL UPDATE THE USERNAME AND EMAIL
                pin_hash = str(random.getrandbits(128))
                new_username = update_details_form.username.data
                new_email = update_details_form.email.data
                print(new_email)
                print(new_username)
                # noinspection PyArgumentList
                update_request = UpdateAuthorizationDetails(
                    pin_hash=pin_hash,
                    user_id=current_user.id,
                    old_username=current_user.username,
                    old_email=current_user.email,
                    new_username=new_username,
                    new_email=new_email
                )
                db.session.add(update_request)
                db.session.commit()
                return redirect(url_for('mfa_authorization', user_id=current_user.id, pin_hash=pin_hash))
    logins_table = []
    for i in LoginUser.query.filter_by(user_ID=current_user.id, status=True).order_by(LoginUser.date.desc()).limit(10):
        logins_table.append(
            {
                'date': str(i.date)[:19],
                'ipAddress': hide_ip(i.ipAddress)
            }
        )
    return render_template(
        "account-user.html",
        title="Account",
        username=current_user.username,
        email=current_user.email,
        member_since=str(current_user.date)[:19],
        logins_table=logins_table,
        form=update_details_form
    )


@app.route("/mfa-authorization/update-details/<user_id>/<pin_hash>/", methods=["GET", "POST"])
@login_required
def mfa_authorization(user_id, pin_hash):
    if str(current_user.id) != user_id:
        return redirect(url_for('account_user'))
    form = AuthorizationForm()
    if form.validate_on_submit() and request.method == "POST":
        totp = pyotp.TOTP(current_user.qrcode_secret)
        if totp.verify(form.pin.data):
            update_details = UpdateAuthorizationDetails.query.filter_by(user_id=user_id, pin_hash=pin_hash, valid=True).first()
            if update_details is not None:
                new_username = update_details.new_username
                new_email = update_details.new_email
                user = User.query.filter_by(id=user_id).first()
                if new_username and new_email:
                    user.username = new_username
                    user.email = new_email
                    user.active = False
                    new_hash = bcrypt.generate_password_hash(str(random.getrandbits(64))).decode('utf-8')
                    user.hash = new_hash
                    update_details.valid = False
                    update_details.used = True
                    db.session.commit()
                    Email().reactivation_email(email=new_email, hash=new_hash, username=new_username)
                    logout_user()
                    flash(f'Your username and email have been updated. Please check the new email provided to reactivate your account.', 'success')
                    return redirect(url_for('home'))
                elif new_username:
                    user.username = new_username
                    update_details.valid = False
                    update_details.used = True
                    db.session.commit()
                    logout_user()
                    login_user(user, remember=False)
                    flash(f'Your username has been updated.', 'success')
                    return redirect(url_for('account_user'))
                elif new_email:
                    user.email = new_email
                    user.active = False
                    new_hash = bcrypt.generate_password_hash(str(random.getrandbits(64))).decode('utf-8')
                    user.hash = new_hash
                    update_details.valid = False
                    update_details.used = True
                    db.session.commit()
                    Email().reactivation_email(email=new_email, hash=new_hash, username=user.username)
                    logout_user()
                    flash(f'Your email has been updated. Please check the new email provided to reactivate your account.', 'success')
                    return redirect(url_for('home'))
                else:
                    # THIS SHOULD NEVER RUN
                    return redirect(url_for('account_user'))
            else:
                return redirect(url_for('account_user'))
        else:
            flash(f'Passcode provided was incorrect, please try again.', 'danger')
            return redirect(url_for("mfa_authorization", user_id=user_id, pin_hash=pin_hash))
    else:
        update_details = UpdateAuthorizationDetails.query.filter_by(user_id=user_id, pin_hash=pin_hash, valid=True).first()
        if update_details is not None:
            old_username = update_details.old_username
            new_username = update_details.new_username
            old_email = update_details.old_email
            new_email = update_details.new_email
            return render_template(
                "qrcodeauthorization.html",
                title="MFA",
                form=form,
                old_username=old_username,
                new_username=new_username,
                old_email=old_email,
                new_email=new_email,
            )
        else:
            return redirect(url_for('account_user'))


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