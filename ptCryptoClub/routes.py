# external imports
from flask import render_template, url_for, flash, redirect, request, session, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, timedelta
import random
import pyotp
import os

# local imports
from ptCryptoClub import app, db, bcrypt
from ptCryptoClub.admin.config import admins_emails, default_delta, default_latest_transactions, default_last_x_hours, default_datapoints, \
    candle_options, default_candle, QRCode, default_transaction_fee, qr_code_folder, default_number_days_buy_sell, available_deltas, \
    CloudWatchLogin, default_fiat, default_news_per_page, mfa_routes, default_playground_candle, candle_values, default_assets_competitions
from ptCryptoClub.admin.models import User, LoginUser, UpdateAuthorizationDetails, ErrorLogs, TransactionsPTCC, Portfolio, PortfolioAssets, \
    ResetPasswordAuthorizations, IpAddressLog, PortfolioRecord, MFA, MFARequests, Reset2FARequests, Competitions, UsersInCompetitions, \
    CompetitionWallet, CompetitionAssets, CompetitionsTransactionsBuy, CompetitionsTransactionsSell
from ptCryptoClub.admin.gen_functions import get_all_markets, get_all_pairs, card_generic, table_latest_transactions, hide_ip, get_last_price, \
    get_pairs_for_portfolio_dropdown, get_quotes_for_portfolio_dropdown, get_available_amount, get_available_amount_sell, get_ptcc_transactions, \
    get_available_assets, calculate_total_value, SecureApi, buy_sell_line_data, hash_generator, get_data_live_chart, get_price, cci, cci_chart, \
    gen_fiats, fiat_line_chart_data, get_all_fiats, get_fiat_name, newsfeed, news_search, count_all_news, get_all_news_source_id, portfolio_chart, \
    portfolio_data_start_info, portfolio_rank_table, my_competitions, future_competitions, ongoing_competitions, competition_portfolio_value, \
    competitions_transactions
from ptCryptoClub.admin.sql.ohlc_functions import line_chart_data, ohlc_chart_data, vtp_chart_data, get_historical_data_line, \
    get_historical_data_ohlc, get_historical_data_vtp
from ptCryptoClub.admin.forms import RegistrationForm, LoginForm, AuthorizationForm, UpdateDetailsForm, BuyAssetForm, SellAssetForm, \
    PasswordRecoveryEmailForm, PasswordRecoveryUsernameForm, PasswordRecoveryConfirmationForm, FirstPinLogin, CreateCompetitionForm, \
    BuyAssetFormCompetition, SellAssetFormCompetition
from ptCryptoClub.admin.auto_email import Email
from ptCryptoClub.admin.admin_functions import admin_main_tables, admin_last_update, admin_api_usage_data, admin_api_details, \
    admin_users_data_sample, admin_api_usage_top_5, admin_users_data, admin_delete_user, admin_ip_info, admin_competition_list
from ptCryptoClub.admin.stats import UsageStats


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=15)


@app.template_filter()
def numberFormat(value):
    return f"{round(value, 8) : ,}"


@app.context_processor
def send_my_func():
    if current_user.is_authenticated:
        api_secret = SecureApi().get_api_secret(user_id=current_user.id)
    else:
        api_secret = SecureApi().get_api_secret(user_id=None)
    return {
        "admins_emails": admins_emails,
        "all_markets": get_all_markets(),
        "default_candle": default_candle,
        "api_secret": api_secret,
        "notUserId": User.query.filter_by(username="notUser").first().id,
        "default_news_per_page": default_news_per_page
    }


@app.route("/")
def home():
    delta = request.args.get('delta')
    if delta is None:
        delta = default_delta
    elif delta not in available_deltas:
        delta = default_delta
    delta = int(delta)
    cards = []
    markets = get_all_markets()
    for market in markets:
        for pair in get_all_pairs(market):
            dict_ = card_generic(base=pair['base'], quote=pair['quote'], market=pair['market'], delta=delta)
            cards.append(dict_)
    tables = []
    number_of_trans = default_latest_transactions
    for market in markets:
        for pair in get_all_pairs(market):
            tables.append(
                table_latest_transactions(base=pair['base'], quote=pair['quote'], market=pair['market'], number_of_trans=number_of_trans)
            )
    if current_user.is_authenticated:
        total_portfolio = calculate_total_value(current_user.id)
        all_markets = get_all_markets()
        markets_choices = []
        for market in all_markets:
            markets_choices.append(
                (market, market)
            )
        form_buy = BuyAssetForm()
        form_buy.market.choices = markets_choices
        form_sell = SellAssetForm()
        form_sell.market_sell.choices = markets_choices
        available_funds = get_available_amount(current_user.id)
        available_assets = get_available_assets(current_user.id)
    else:
        total_portfolio = {}
        form_buy = None
        form_sell = None
        available_funds = 0
        available_assets = []
    return render_template(
        "index.html",
        title="Home",
        cards=cards,
        tables=tables,
        number_of_trans=number_of_trans,
        total_portfolio=total_portfolio,
        form_buy=form_buy,
        form_sell=form_sell,
        available_funds=available_funds,
        default_transaction_fee=default_transaction_fee,
        available_assets=available_assets,
        delta=delta,
        number_days_buy_sell=default_number_days_buy_sell,
        fiats_data=gen_fiats(delta=delta),
        available_deltas=available_deltas
    )


@app.route("/api/home/cards/<base>/<quote>/<market>/<delta>/<api_secret>/")
def api_home_cards(base, quote, market, delta, api_secret):
    if SecureApi().validate(api_secret=api_secret):
        return jsonify(
            card_generic(base=base, quote=quote, market=market, delta=delta)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/home/latest-transactions/<base>/<quote>/<market>/<number_of_trans>/<api_secret>/")
def api_home_latest_transactions(base, quote, market, number_of_trans, api_secret):
    if SecureApi().validate(api_secret=api_secret):
        return jsonify(
            table_latest_transactions(base=base, quote=quote, market=market, number_of_trans=number_of_trans)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/home/cci/<market1>/<base1>/<quote1>/<market2>/<base2>/<quote2>/<delta>/<api_secret>/")
def api_home_cci_gauge(market1, base1, quote1, market2, base2, quote2, delta, api_secret):
    if SecureApi().validate(api_secret=api_secret):
        return jsonify(
            cci(market_1=market1, base_1=base1, quote_1=quote1, market_2=market2, base_2=base2, quote_2=quote2, delta=delta)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/home/cci/chart/<market1>/<base1>/<quote1>/<market2>/<base2>/<quote2>/<datapoints>/<api_secret>/")
def api_home_cci_chart(market1, base1, quote1, market2, base2, quote2, datapoints, api_secret):
    if SecureApi().validate(api_secret=api_secret):
        return jsonify(
            cci_chart(market1, base1, quote1, market2, base2, quote2, int(datapoints))
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/home/fiat-prices/<delta>/<api_secret>/")
def api_home_fiat_prices(delta, api_secret):
    if SecureApi().validate(api_secret=api_secret):
        return jsonify(
            gen_fiats(delta=delta)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/home/newsfeed/<n>/<api_secret>/")
def api_home_newsfeed(n, api_secret):
    if SecureApi().validate(api_secret=api_secret, exception=True):
        return jsonify(
            newsfeed(n=n)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/price/<market>/<base_1>/<base_2>/<quote>/<data_points>/<api_secret>/")
def api_price(market, base_1, base_2, quote, data_points, api_secret):
    if SecureApi().validate(api_secret=api_secret):
        return jsonify(
            get_price(market, base_1, base_2, quote, data_points)
        )
    else:
        return jsonify(
            {}
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
            elif bcrypt.check_password_hash(user.password, password):
                mfa_active = MFA.query.filter_by(user_id=user.id).first()
                if mfa_active is None:
                    mfa = True
                else:
                    if mfa_active.mfa:
                        mfa = True
                    else:
                        mfa = False
                if mfa:
                    if totp.verify(given_code):
                        login_user(user, remember=False)
                        # noinspection PyArgumentList
                        log = LoginUser(user_ID=user.id,
                                        ipAddress=request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
                                        status=True)
                        db.session.add(log)
                        db.session.commit()
                        return redirect(url_for('first_time_pin_change'))
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
                    if bcrypt.check_password_hash(mfa_active.r_pin, given_code):
                        login_user(user, remember=False)
                        # noinspection PyArgumentList
                        log = LoginUser(user_ID=user.id,
                                        ipAddress=request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
                                        status=True)
                        db.session.add(log)
                        db.session.commit()
                        return redirect(url_for('first_time_pin_change'))
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
            hash_1 = request.args.get('hash_1')
            hash_2 = request.args.get('hash_2')
            secret = request.args.get('secret')
            db_request = Reset2FARequests.query.filter_by(id=secret, hash_1=hash_1, hash_2=hash_2).first()
            if db_request is None:
                Email().activation_email(email=user.email, hash=user.hash, username=user.username)
                flash(f'Your account has been create. Please check your email to activate your account.', 'success')
            else:
                flash(f'2FA has been successfully reset in your account.', 'success')
            os.remove(qr_code_folder + user.qrcode_img + '.png')
            user.active_qr = True
            user.qrcode_img = None
            db.session.commit()
            return redirect(url_for('home'))
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


@app.route('/activate-account/')
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
                    # noinspection PyArgumentList
                    new_portfolio = Portfolio(
                        user_id=user.id
                    )
                    db.session.add(new_portfolio)
                    for market in get_all_markets():
                        for pair in get_pairs_for_portfolio_dropdown(market)[1:]:
                            # noinspection PyArgumentList
                            new_portfolio_assets = PortfolioAssets(
                                user_id=user.id,
                                asset=pair['base']
                            )
                            db.session.add(new_portfolio_assets)
                    port_record = calculate_total_value(user_id=user.id)
                    # noinspection PyArgumentList
                    new_record = PortfolioRecord(
                        user_id=user.id,
                        value=port_record["value"],
                        wallet=port_record["wallet"],
                        assets=port_record["assets"],
                        percentage=port_record["percentage"]
                    )
                    db.session.add(new_record)
                    db.session.commit()
                    flash(f'Your account has been activated.', 'success')
                    return redirect(url_for('login'))
            else:
                flash(f'Your activation details are incorrect, please try again.', 'danger')
                return redirect(url_for('home'))
        else:
            flash(f'Your activation details are incorrect, please try again.', 'danger')
            return redirect(url_for('home'))


@app.route("/W79MS82B0nr5x9i2CSsg05bhy0M09x0B77E1hJSvj4hB6591PBQv8vDoy2/", methods=["GET", "POST"])
def recovery_2FA():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        form = PasswordRecoveryEmailForm()
        if request.method == "POST":
            if form.validate_on_submit():
                email = form.email.data
                user = User.query.filter_by(email=email).first()
                if user is not None:
                    check_old = Reset2FARequests.query.filter_by(user_id=user.id, valid=True).first()
                    if check_old is not None:
                        if datetime.utcnow() <= check_old.date + timedelta(seconds=300):
                            # There is a valid request so no action is needed
                            pass
                        else:
                            check_old.valid = False
                            hash_1 = hash_generator(LENGTH=random.randint(50, 200))
                            hash_2 = hash_generator(LENGTH=random.randint(100, 200))
                            # noinspection PyArgumentList
                            line = Reset2FARequests(
                                user_id=user.id,
                                hash_1=hash_1,
                                hash_2=hash_2
                            )
                            db.session.add(line)
                            db.session.commit()
                            Email().request_2fa_reset(email=user.email, username=user.username, user_id=user.id, hash_1=hash_1, hash_2=hash_2)
                    else:
                        hash_1 = hash_generator(LENGTH=random.randint(50, 200))
                        hash_2 = hash_generator(LENGTH=random.randint(100, 200))
                        # noinspection PyArgumentList
                        line = Reset2FARequests(
                            user_id=user.id,
                            hash_1=hash_1,
                            hash_2=hash_2
                        )
                        db.session.add(line)
                        db.session.commit()
                        Email().request_2fa_reset(email=user.email, username=user.username, user_id=user.id, hash_1=hash_1, hash_2=hash_2)
                else:
                    # No feedback will be given
                    pass
            else:
                # No feedback will be given
                pass
            flash(f'An email has been sent, please check your inbox for further instructions.', 'success')
            return redirect(url_for("recovery_2FA"))
        else:
            return render_template(
                "recovery-2FA.html",
                title="Reset 2FA",
                form=form
            )


@app.route(f"/account/{mfa_routes['reset_2fa_confirmation']}/<hash_1>/<user_id>/<hash_2>/")
def recovery_2FA_confirmation(hash_1, user_id, hash_2):
    if current_user.is_authenticated:
        logout_user()
    db_request = Reset2FARequests.query.filter_by(user_id=user_id, hash_1=hash_1, hash_2=hash_2).first()
    if db_request is None:
        return redirect(url_for("home"))
    else:
        if datetime.utcnow() > db_request.date + timedelta(seconds=300):
            flash("This link has expired.", "warning")
            return redirect(url_for("home"))
        else:
            user = User.query.filter_by(id=user_id).first()
            qrcode_secret = pyotp.random_base32()
            url = pyotp.totp.TOTP(qrcode_secret).provisioning_uri(name=user.username, issuer_name='app.ptcrypto.club')
            filename = str(random.getrandbits(64))
            QRCode(info=url, filename=filename)
            user.active_qr = False
            user.qrcode_secret = qrcode_secret
            user.qrcode_img = filename
            db_request.used = True
            db_request.valid = False
            db.session.commit()
            return redirect(url_for('qr_activation', ID=filename, hash_1=hash_1, hash_2=hash_2, secret=db_request.id))


@app.route("/recovery/password/email/", methods=["GET", "POST"])
def password_recovery_email():
    logout_user()
    form = PasswordRecoveryEmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            # check for existing authorizations
            old_auths = ResetPasswordAuthorizations.query.filter_by(user_id=user.id, valid=True)
            if old_auths is not None:
                for old_auth in old_auths:
                    old_auth.valid = False
                db.session.commit()
            hash = hash_generator(random.randint(150, 200))
            # noinspection PyArgumentList
            authorization = ResetPasswordAuthorizations(
                user_id=user.id,
                hash=hash
            )
            db.session.add(authorization)
            db.session.commit()
            Email().password_recovery_email(email=user.email, hash=hash, username=user.username, user_id=user.id)
            flash("Please check your email inbox. An email has been sent with instructions to recover your password.", "success")
            return redirect(url_for('home'))
        else:
            flash("Email not found! Please enter the email address used to create your account.", "danger")
            return redirect(url_for('password_recovery_email'))
    else:
        return render_template(
            "password-recovery-email.html",
            title="Password recovery",
            form=form
        )


@app.route("/recovery/password/username/", methods=["GET", "POST"])
def password_recovery_username():
    logout_user()
    form = PasswordRecoveryUsernameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            # check for existing authorizations
            old_auths = ResetPasswordAuthorizations.query.filter_by(user_id=user.id, valid=True)
            if old_auths is not None:
                for old_auth in old_auths:
                    old_auth.valid = False
                db.session.commit()
            hash = hash_generator(random.randint(150, 200))
            # noinspection PyArgumentList
            authorization = ResetPasswordAuthorizations(
                user_id=user.id,
                hash=hash
            )
            db.session.add(authorization)
            db.session.commit()
            Email().password_recovery_email(email=user.email, hash=hash, username=user.username, user_id=user.id)
            flash("Please check your email inbox. An email has been sent with instructions to recover your password.", "success")
            return redirect(url_for('home'))
        else:
            flash("Username not found! Please enter your username.", "danger")
            return redirect(url_for('password_recovery_username'))
    else:
        return render_template(
            "password-recovery-username.html",
            title="Password recovery",
            form=form
        )


@app.route("/recovery/password/confirmation/<hash>/<user_id>/", methods=["GET", "POST"])
def password_recovery_confirmation(hash, user_id):
    logout_user()
    form = PasswordRecoveryConfirmationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            flash("Details are incorrect, please try again.", "warning")
            return redirect(url_for('home'))
        else:
            # check db for authorization
            authorization = ResetPasswordAuthorizations.query.filter_by(
                hash=hash,
                user_id=user.id,
                valid=True
            ).first()
            if authorization is None:
                flash("Details are incorrect, please try again.", "warning")
                return redirect(url_for('home'))
            else:
                delta = datetime.utcnow() - authorization.date_created
                if delta.total_seconds() <= 300:
                    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                    authorization.valid = False
                    authorization.used = True
                    user.password = hashed_password
                    mfa = MFA.query.filter_by(user_id=user.id).first()
                    if mfa is not None:
                        mfa.mfa = True
                        mfa.date = datetime.utcnow()
                    db.session.commit()
                    flash("Your password has been updated.", "success")
                    return redirect(url_for('login'))
                else:
                    authorization.valid = False
                    db.session.commit()
                    flash("Your request has expired, please try again.", "warning")
                    return redirect(url_for('password_recovery_email'))
    else:
        return render_template(
            "password-recovery-confirmation.html",
            title="Password recovery",
            form=form,
            hash=hash,
            user_id=user_id
        )


@app.route("/recovery/password/request/")
@login_required
def password_recovery_request():
    old_auths = ResetPasswordAuthorizations.query.filter_by(user_id=current_user.id, valid=True)
    if old_auths is not None:
        for old_auth in old_auths:
            old_auth.valid = False
        db.session.commit()
    hash = hash_generator(random.randint(150, 200))
    # noinspection PyArgumentList
    authorization = ResetPasswordAuthorizations(
        user_id=current_user.id,
        hash=hash
    )
    db.session.add(authorization)
    db.session.commit()
    Email().password_recovery_email(email=current_user.email, hash=hash, username=current_user.username, user_id=current_user.id)
    logout_user()
    flash("Please check your email inbox. An email has been sent with instructions to change your password.", "info")
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
    mfa_active = MFA.query.filter_by(user_id=current_user.id).first()
    if mfa_active is None:
        mfa = True
    else:
        if mfa_active.mfa:
            mfa = True
        else:
            mfa = False
    return render_template(
        "account-user.html",
        title="Account",
        username=current_user.username,
        email=current_user.email,
        member_since=str(current_user.date)[:19],
        logins_table=logins_table,
        form=update_details_form,
        mfa=mfa
    )


@app.route("/account/g7KHjWT0YDY5ufo243FYzWCc2WvS522HePt4im2ymFP/<user_id>/<key>/")
def deactivate_2fa(user_id, key):
    try:
        user_id = int(user_id)
    except Exception as e:
        print(e)  # an error log will not be created
        flash(f'Invalid url!', 'danger')
        return redirect(url_for("account_user"))
    user = User.query.filter_by(
        id=user_id,
        api_secret=key
    ).first()
    if user is not None:
        mfa_request = MFARequests.query.filter_by(user_id=user.id, valid=True, deactivate=True).first()
        if mfa_request is not None:
            if datetime.utcnow() <= mfa_request.date + timedelta(seconds=300):
                flash(f"A request has already been made, please check your email.", "warning")
            else:
                mfa_request.valid = False
                db.session.commit()
                return redirect(url_for("deactivate_2fa", user_id=user_id, key=key))
        else:
            hash = hash_generator(LENGTH=random.randint(150, 200))
            # noinspection PyArgumentList
            authorization = MFARequests(
                user_id=user.id,
                hash=hash,
                deactivate=True
            )
            db.session.add(authorization)
            db.session.commit()
            Email().deactivate_2fa(email=user.email, hash=hash, username=user.username, user_id=user.id)
            flash(f'An email has been sent, please check your inbox.', 'success')
        return redirect(url_for("account_user"))
    else:
        flash(f'Invalid url!', 'danger')
        return redirect(url_for("account_user"))


@app.route(f"/account/{mfa_routes['deactivate_2fa_confirmation']}/<hash>/<user_id>/")
def deactivate_2fa_confirmation(hash, user_id):
    mfa_request = MFARequests.query.filter_by(user_id=user_id, hash=hash, valid=True, deactivate=True).first()
    if mfa_request is not None:
        if datetime.utcnow() > mfa_request.date + timedelta(seconds=300):
            mfa_request.valid = False
            db.session.commit()
            flash(f'This link is no longer valid.', 'danger')
            return redirect(url_for("account_user"))
        else:
            mfa_request.valid = False
            mfa_request.used = True
            mfa_deactivate = MFA.query.filter_by(user_id=user_id).first()
            pin = "".join(random.choice("0123456789") for _ in range(6))
            hashed_pin = bcrypt.generate_password_hash(pin).decode('utf-8')
            if mfa_deactivate is None:
                # noinspection PyArgumentList
                mfa_deactivate = MFA(
                    user_id=user_id,
                    mfa=False,
                    r_pin=hashed_pin,
                    date=datetime.utcnow(),
                    first_login=True
                )
                db.session.add(mfa_deactivate)
            else:
                mfa_deactivate.date = datetime.utcnow()
                mfa_deactivate.mfa = False
                mfa_deactivate.r_pin = hashed_pin
                mfa_deactivate.first_login = True
            db.session.commit()
            user = User.query.filter_by(id=user_id).first()
            Email().pin_2fa(email=user.email, username=user.username, pin=pin)
            flash(f'2FA at login has been deactivated from your account and an email with your access pin has been sent.', 'success')
            return redirect(url_for("account_user"))
    else:
        return redirect(url_for("home"))


@app.route("/account/nI0CmSJAt0A48WPV4HM262ZsS5JXtPEQsC3s7LVuD0/<user_id>/<key>/")
def activate_2fa(user_id, key):
    try:
        user_id = int(user_id)
    except Exception as e:
        print(e)  # an error log will not be created
        flash(f'Invalid url!', 'danger')
        return redirect(url_for("account_user"))
    user = User.query.filter_by(
        id=user_id,
        api_secret=key
    ).first()
    if user is not None:
        mfa_request = MFARequests.query.filter_by(user_id=user.id, valid=True, deactivate=False).first()
        if mfa_request is not None:
            if datetime.utcnow() <= mfa_request.date + timedelta(seconds=300):
                flash(f"A request has already been made, please check your email.", "warning")
            else:
                mfa_request.valid = False
                db.session.commit()
                return redirect(url_for("activate_2fa", user_id=user_id, key=key))
        else:
            hash = hash_generator(LENGTH=random.randint(150, 200))
            # noinspection PyArgumentList
            authorization = MFARequests(
                user_id=user.id,
                hash=hash,
                deactivate=False
            )
            db.session.add(authorization)
            db.session.commit()
            Email().activate_2fa(email=user.email, hash=hash, username=user.username, user_id=user.id)
            flash(f'An email has been sent, please check your inbox.', 'success')
        return redirect(url_for("account_user"))
    else:
        flash(f'Invalid url!', 'danger')
        return redirect(url_for("account_user"))


@app.route(f"/account/{mfa_routes['activate_2fa_confirmation']}/<hash>/<user_id>/")
def activate_2fa_confirmation(hash, user_id):
    mfa_request = MFARequests.query.filter_by(user_id=user_id, hash=hash, valid=True, deactivate=False).first()
    if mfa_request is not None:
        if datetime.utcnow() > mfa_request.date + timedelta(seconds=300):
            mfa_request.valid = False
            db.session.commit()
            flash(f'This link is no longer valid.', 'danger')
            return redirect(url_for("account_user"))
        else:
            mfa_request.valid = False
            mfa_request.used = True
            mfa_activate = MFA.query.filter_by(user_id=user_id).first()
            if mfa_activate is not None:
                mfa_activate.mfa = True
                mfa_activate.date = datetime.utcnow()
                mfa_activate.first_login = False
            db.session.commit()
            flash(f'2FA at login has been reactivated from your account.', 'success')
            return redirect(url_for("account_user"))
    else:
        return redirect(url_for("home"))


@app.route("/A9hQDxZeu3Yc03rSaaMepCpCQDYc03urSqFxZqFaaM9h/", methods=["GET", "POST"])
@login_required
def first_time_pin_change():
    test = MFA.query.filter_by(user_id=current_user.id).first()
    if test is None:
        return redirect(url_for("portfolio"))
    else:
        if not test.first_login:
            return redirect(url_for("portfolio"))
        else:
            form = FirstPinLogin()
            if form.validate_on_submit():
                new_pin = form.new_pin.data
                hashed_pin = bcrypt.generate_password_hash(new_pin).decode('utf-8')
                test.r_pin = hashed_pin
                test.first_login = False
                db.session.commit()
                flash(f'Your PIN has been changed.', 'success')
                return redirect(url_for("portfolio"))
            else:
                return render_template(
                    "pin-change.html",
                    title="Change default pin",
                    form=form
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


@app.route("/account/admin/")
@login_required
def account_admin():
    if current_user.email not in admins_emails:
        return redirect(url_for("account_user"))
    else:
        # THIS NEEDS TO BE REVIEWED REALLY BAD SOLUTION #
        raw_ip_list = IpAddressLog.query.with_entities(IpAddressLog.ip_address).order_by(IpAddressLog.date.desc()).distinct()
        ip_list_7 = []
        for t in raw_ip_list:
            if t[0] not in ip_list_7:
                ip_list_7.append(t[0])
            else:
                pass
            if len(ip_list_7) == 7:
                break
        ip_list = [admin_ip_info(ip_address=t, full_info=False) for t in ip_list_7]
        #################################################
        # next line will delete any competition that is not live and the start date is in the past #
        Competitions.query.filter(Competitions.start_date < datetime.utcnow(), Competitions.is_live == False).delete() # PEP8 exception
        db.session.commit()
        return render_template(
            "account-admin.html",
            title="Account",
            table_data=admin_main_tables(),
            last_update=admin_last_update(),
            users_sample=admin_users_data_sample(),
            ip_list=ip_list,
            competition_list=admin_competition_list(limit=5)
        )


@app.route("/account/admin/api-info/")
@login_required
def account_admin_api_info():
    if current_user.email not in admins_emails:
        return redirect(url_for("account_user"))
    else:
        return render_template(
            "account-admin-api-info.html",
            title="Api info"
        )


@app.route("/account/admin/users/<page>/")
@login_required
def account_admin_users(page):
    if current_user.email not in admins_emails:
        return redirect(url_for("account_user"))
    else:
        user_data, c_page, last_page = admin_users_data(page=page)
        return render_template(
            "account-admin-users.html",
            title="Api info",
            user_data=user_data,
            c_page=c_page,
            last_page=last_page
        )


@app.route("/account/admin/delete/user/<user_id>/")
@login_required
def account_admin_delete_user(user_id):
    if current_user.email not in admins_emails:
        return redirect(url_for("account_user"))
    else:
        admin_delete_user(user_id)
        return redirect(url_for("account_admin_users", page=1))


@app.route("/account/admin/ip-info/")
@login_required
def account_admin_ip_info():
    if current_user.email not in admins_emails:
        return redirect(url_for("account_user"))
    else:
        # THIS NEEDS TO BE REVIEWED REALLY BAD SOLUTION
        raw_ip_list = IpAddressLog.query.with_entities(IpAddressLog.ip_address).order_by(
            IpAddressLog.date.desc()).distinct()
        full_list = []
        for t in raw_ip_list:
            if t[0] not in full_list:
                full_list.append(t[0])
            else:
                pass
        # full_list = [t[0] for t in raw_ip_list if t[0] not in full_list]
        return render_template(
            "account-admin-ip-info.html",
            title="IP info",
            full_list=full_list
        )


@app.route("/account/admin/create-competition/", methods=["GET", "POST"])
@login_required
def account_admin_create_competition():
    if current_user.email not in admins_emails:
        return redirect(url_for("account_user"))
    else:
        form = CreateCompetitionForm()
        competition_id = request.args.get('edit')
        if competition_id is not None:
            competition_to_edit = Competitions.query.filter_by(id=competition_id, is_live=False).first()
            if competition_to_edit is None:
                return redirect(url_for("account_user"))
            else:
                if request.method == "POST":
                    if form.validate_on_submit():
                        if form.max_users.data == "":
                            m_users = None
                        else:
                            m_users = form.max_users.data
                        if form.users.data == "0":
                            t_users = None
                        else:
                            t_users = form.users.data
                        competition_to_edit.name = form.name.data
                        competition_to_edit.modified_by = current_user.id
                        competition_to_edit.date_modified = datetime.utcnow()
                        competition_to_edit.start_date = form.start_date.data
                        competition_to_edit.end_date = form.end_date.data
                        competition_to_edit.start_amount = form.amount.data
                        competition_to_edit.amount_quote = form.quote.data
                        competition_to_edit.buy_fee = form.buy_fee.data
                        competition_to_edit.sell_fee = form.sell_fee.data
                        competition_to_edit.max_users = m_users
                        competition_to_edit.type_users = t_users
                        competition_to_edit.send_email = form.p_email.data
                        db.session.commit()
                        return redirect(url_for('account_admin'))

                    else:
                        return render_template(
                            "account-admin-create-competition.html",
                            title="Create competition",
                            form=form
                        )
                else:
                    form.name.data = competition_to_edit.name
                    form.start_date.data = competition_to_edit.start_date
                    form.end_date.data = competition_to_edit.end_date
                    form.amount.data = competition_to_edit.start_amount
                    form.quote.data = competition_to_edit.amount_quote
                    form.buy_fee.data = competition_to_edit.buy_fee
                    form.sell_fee.data = competition_to_edit.sell_fee
                    form.max_users.data = competition_to_edit.max_users
                    form.users.data = competition_to_edit.type_users
                    form.p_email.data = competition_to_edit.send_email
                    return render_template(
                        "account-admin-create-competition.html",
                        title="Create competition",
                        form=form
                    )
        else:
            if form.validate_on_submit():
                if form.max_users.data == "":
                    m_users = None
                else:
                    m_users = form.max_users.data
                if form.users.data == '0':
                    t_users = None
                else:
                    t_users = form.users.data
                # noinspection PyArgumentList
                new_competition = Competitions(
                    name=form.name.data,
                    created_by=current_user.id,
                    start_date=form.start_date.data,
                    end_date=form.end_date.data,
                    start_amount=form.amount.data,
                    amount_quote=form.quote.data,
                    buy_fee=form.buy_fee.data,
                    sell_fee=form.sell_fee.data,
                    max_users=m_users,
                    type_users=t_users,
                    send_email=form.p_email.data,
                )
                db.session.add(new_competition)
                db.session.commit()
                return redirect(url_for('account_admin'))
            return render_template(
                "account-admin-create-competition.html",
                title="Create competition",
                form=form
            )


@app.route("/account/admin/competition/review/<comp_id>/", methods=["GET", "POST"])
@login_required
def account_admin_create_competition_review(comp_id):
    if current_user.email not in admins_emails:
        return redirect(url_for("account_user"))
    else:
        to_review = Competitions.query.filter_by(id=comp_id).first()
        if to_review is not None:
            form = AuthorizationForm()
            if request.method == "POST":
                if form.validate_on_submit():
                    secret = current_user.qrcode_secret
                    totp = pyotp.TOTP(secret)
                    if totp.verify(form.pin.data):
                        to_review.is_live = True
                        db.session.commit()
                        flash("Competition is now live and visible to users.", "success")
                        return redirect(url_for("account_admin"))
                    else:
                        flash("2FA is not correct, please try again.", "danger")
                        return redirect(url_for("account_admin_create_competition_review", comp_id=comp_id))
                else:
                    return redirect(url_for("account_admin_create_competition_review", comp_id=comp_id))
            else:
                info = {
                    "id": to_review.id,
                    "name": to_review.name,
                    "start_date": to_review.start_date,
                    "end_date": to_review.end_date,
                    "start_amount": to_review.start_amount,
                    "amount_quote": to_review.amount_quote,
                    "buy_fee": to_review.buy_fee,
                    "sell_fee": to_review.sell_fee,
                    "max_users": to_review.max_users,
                    "type_users": to_review.type_users,
                    "send_email": to_review.send_email,
                    "is_live": to_review.is_live
                }
                return render_template(
                    "account-admin-create-competition-review.html",
                    title="Competition review",
                    info=info,
                    comp_id=comp_id,
                    form=form
                )
        else:
            return redirect(url_for("account_user"))


@app.route("/account/admin/competition/delete/<comp_id>/")
@login_required
def account_admin_create_competition_delete(comp_id):
    to_delete = Competitions.query.filter_by(id=comp_id).first()
    if to_delete is not None:
        if to_delete.is_live:
            flash("You cannot delete a live competition", "danger")
            return redirect(url_for("account_admin"))
        else:
            Competitions.query.filter_by(id=comp_id).delete()
            db.session.commit()
            flash("Competition deleted", "success")
            return redirect(url_for("account_admin"))
    else:
        return redirect(url_for("account_user"))


@app.route("/api/admin/live-data/<api_secret>/")
def api_admin_live_data(api_secret):
    if SecureApi().validate(api_secret=api_secret, admin=True):
        return jsonify(
            admin_last_update()
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/admin/api-usage/<api_secret>/")
def api_admin_api_usage(api_secret):
    if SecureApi().validate(api_secret=api_secret, admin=True):
        return jsonify(
            admin_api_usage_data()
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/admin/api-usage/details/<api_secret>/")
def api_admin_api_usage_details(api_secret):
    if SecureApi().validate(api_secret=api_secret, admin=True):
        return jsonify(
            admin_api_details()
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/admin/api-usage/top-5/<api_secret>/")
def api_admin_api_usage_top_5(api_secret):
    if SecureApi().validate(api_secret=api_secret, admin=True):
        return jsonify(
            admin_api_usage_top_5()
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/admin/cpu-usage/webserver/<api_secret>/")
def api_admin_cpu_usage_webserver(api_secret):
    if SecureApi().validate(api_secret=api_secret, admin=True):
        return jsonify(
            UsageStats().cpu_utilization_ec2(instance=CloudWatchLogin.webserver)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/admin/cpu-usage/data-creator/<api_secret>/")
def api_admin_cpu_usage_data_creator(api_secret):
    if SecureApi().validate(api_secret=api_secret, admin=True):
        return jsonify(
            UsageStats().cpu_utilization_ec2(instance=CloudWatchLogin.data_creator)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/admin/cpu-usage/database/<api_secret>/")
def api_admin_cpu_usage_db(api_secret):
    if SecureApi().validate(api_secret=api_secret, admin=True):
        return jsonify(
            UsageStats().cpu_utilization_db(instance=CloudWatchLogin.database)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/admin/free-ram/database/<api_secret>/")
def api_admin_free_ram_db(api_secret):
    if SecureApi().validate(api_secret=api_secret, admin=True):
        return jsonify(
            UsageStats().ram_utilization_db(instance=CloudWatchLogin.database)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/admin/connections/database/<api_secret>/")
def api_admin_connections_db(api_secret):
    if SecureApi().validate(api_secret=api_secret, admin=True):
        return jsonify(
            UsageStats().connections_db(instance=CloudWatchLogin.database)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/admin/ip-info/<ip>/<api_secret>/")
def api_admin_ip_info(ip, api_secret):
    if SecureApi().validate(api_secret=api_secret, admin=True):
        return jsonify(
            admin_ip_info(ip_address=ip, full_info=True)
        )
    else:
        return jsonify(
            {}
        )


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


@app.route("/api/market/chart/live/<market>/<base>/<quote>/<datapoints>/<api_secret>/")
def api_market_chart_live(market, base, quote, datapoints, api_secret):
    if SecureApi().validate(api_secret=api_secret):
        return jsonify(
            get_data_live_chart(market=market, base=base, quote=quote, data_points=datapoints, delta=20)
        )
    else:
        return jsonify(
            {}
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


@app.route("/api/line-chart/info/<market>/<base>/<quote>/<delta>/<api_secret>/")
def api_charts_line_info(market, base, quote, delta, api_secret):
    if SecureApi().validate(api_secret=api_secret):
        return jsonify(
            card_generic(base, quote, market, delta)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/charts/line/<market>/<base>/<quote>/<last_x_hours>/<api_secret>/")
def api_charts_line_data(market, base, quote, last_x_hours, api_secret):
    if SecureApi().validate(api_secret=api_secret):
        return jsonify(
            line_chart_data(base, quote, market, last_x_hours)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/charts/ohlc/<market>/<base>/<quote>/<candle>/")
def chart_ohlc(market, base, quote, candle):
    try:
        candle = int(candle)
    except Exception as e:
        print(e)
        candle = default_candle
    if candle == 20:
        candle_in_use_display = "20 sec"
    elif candle == 60:
        candle_in_use_display = "01 min"
    elif candle == 300:
        candle_in_use_display = "05 min"
    elif candle == 900:
        candle_in_use_display = "15 min"
    elif candle == 1800:
        candle_in_use_display = "30 min"
    elif candle == 3600:
        candle_in_use_display = "01 hour"
    else:
        return redirect(url_for('chart_ohlc', market=market, base=base, quote=quote, candle=default_candle))
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


@app.route("/api/charts/ohlc/<market>/<base>/<quote>/<datapoints>/<candle>/<api_secret>/")
def api_charts_ohlc_data(market, base, quote, datapoints, candle, api_secret):
    if SecureApi().validate(api_secret=api_secret):
        return jsonify(
            ohlc_chart_data(base, quote, market, datapoints, candle)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/charts/vtp/<market>/<base>/<quote>/<candle>/")
def chart_vtp(market, base, quote, candle):
    try:
        candle = int(candle)
    except Exception as e:
        print(e)
        candle = default_candle
    if candle == 20:
        candle_in_use_display = "20 sec"
    elif candle == 60:
        candle_in_use_display = "1 min"
    elif candle == 300:
        candle_in_use_display = "5 min"
    elif candle == 900:
        candle_in_use_display = "15 min"
    elif candle == 1800:
        candle_in_use_display = "30 min"
    elif candle == 3600:
        candle_in_use_display = "01 hour"
    else:
        return redirect(url_for('chart_vtp', market=market, base=base, quote=quote, candle=default_candle))
    return render_template(
        "charts-vtp.html",
        title="Charts",
        market=market,
        base=base,
        quote=quote,
        datapoints=default_datapoints,
        candles=candle_options,
        candle_in_use=candle,
        candle_in_use_display=candle_in_use_display
    )


@app.route("/api/charts/vtp/<market>/<base>/<quote>/<datapoints>/<candle>/<api_secret>/")
def api_charts_vtp_data(market, base, quote, datapoints, candle, api_secret):
    if SecureApi().validate(api_secret=api_secret):
        return jsonify(
            vtp_chart_data(base, quote, market, datapoints, candle)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/charts/fiat/<fiat>/")  # DO NOT CHANGE THE URL
def chart_line_fiat(fiat):
    if fiat.upper() not in get_all_fiats():
        fiat = default_fiat
    name = get_fiat_name(fiat=fiat.upper())
    return render_template(
        "charts-fiat-line.html",
        title="Charts",
        fiat=fiat,
        name=name
    )


@app.route("/api/charts/fiat/line/<fiat>/<delta>/<api_secret>/")
def api_charts_fiat_line_data(fiat, delta, api_secret):
    if SecureApi().validate(api_secret=api_secret):
        return jsonify(
            fiat_line_chart_data(fiat=fiat, delta=delta)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/account/portfolio/", methods=["GET", "POST"])
@login_required
def portfolio():
    all_markets = get_all_markets()
    markets_choices = []
    for market in all_markets:
        markets_choices.append(
            (market, market)
        )
    form_buy = BuyAssetForm()
    form_buy.market.choices = markets_choices
    form_sell = SellAssetForm()
    form_sell.market_sell.choices = markets_choices

    buy_transactions = get_ptcc_transactions(user_ID=current_user.id, type_='buy', limit=5)
    sell_transactions = get_ptcc_transactions(user_ID=current_user.id, type_='sell', limit=5)

    available_assets = get_available_assets(current_user.id)
    total_portfolio = calculate_total_value(current_user.id)
    return render_template(
        "portfolio-home.html",
        title="Account",
        form_buy=form_buy,
        form_sell=form_sell,
        available_funds=get_available_amount(current_user.id),
        available_assets=available_assets,
        default_transaction_fee=default_transaction_fee,
        buy_transactions=buy_transactions,
        sell_transactions=sell_transactions,
        total_portfolio=total_portfolio,
        number_days_buy_sell=default_number_days_buy_sell
    )


@app.route("/account/portfolio/details/")
@login_required
def portfolio_details():
    data_full = portfolio_data_start_info(current_user.id)
    return render_template(
        "portfolio-details.html",
        title="Account",
        data_full=data_full
    )


@app.route("/account/portfolio/rank/")
@login_required
def portfolio_rank():
    table = portfolio_rank_table()
    return render_template(
        "portfolio-rank.html",
        title="Hall of Fame",
        table=table
    )


@app.route("/account/portfolio/buy/", methods=["POST"])
@login_required
def portfolio_buy():
    form = BuyAssetForm()
    try:
        market = str(form.market.data)
        base = str(form.base.data)
        quote = str(form.quote.data)
        amount = float(form.amount_spent.data)
    except Exception as e:
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route=f'portfolio buy',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
        flash("Something went wrong, please try again later.", "danger")
        return redirect(url_for('portfolio'))
    if market not in get_all_markets():
        market = None
    validate = False
    for item in get_all_pairs(market):
        if market == item['market'] and base == item['base'] and quote == item['quote']:
            validate = True
            break
    if validate:
        if amount > get_available_amount(current_user.id):
            flash("You don't have enough funds in your wallet.", "warning")
            return redirect(url_for('portfolio'))
        else:
            asset_price = get_last_price(base=base, quote=quote, market=market)['price']
            fee = round(amount * default_transaction_fee, 2)
            asset_amount = round((amount - fee) / asset_price, 8)
            # noinspection PyArgumentList
            new_transaction = TransactionsPTCC(
                user_id=current_user.id,
                type="buy",
                market=market,
                base=base,
                quote=quote,
                asset_amount=asset_amount,
                asset_price=asset_price,
                value=amount,
                fee=fee
            )
            db.session.add(new_transaction)
            db.session.commit()
            user_portfolio = Portfolio().query.filter_by(user_id=current_user.id).first()
            user_portfolio_assets = PortfolioAssets().query.filter_by(user_id=current_user.id)
            for asset_line in user_portfolio_assets:
                if asset_line.asset == base:
                    asset_line.amount = round((asset_line.amount + asset_amount), 8)
                    break
            user_portfolio.wallet = round((user_portfolio.wallet - amount), 8)
            db.session.commit()
            flash(f"Your transaction has been completed.", "success")
            return redirect(url_for('portfolio'))
    else:
        flash("Error, please try again.", "danger")
        return redirect(url_for('portfolio'))


@app.route("/account/portfolio/sell/", methods=["POST"])
@login_required
def portfolio_sell():
    form = SellAssetForm()
    try:
        market = str(form.market_sell.data)
        base = str(form.base_sell.data)
        quote = str(form.quote_sell.data)
        amount_to_be_sold = float(form.amount_spent_sell.data)
    except Exception as e:
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route=f'portfolio sell',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
        flash("Something went wrong, please try again later.", "danger")
        return redirect(url_for('portfolio'))
    if market not in get_all_markets():
        market = None
    validate = False
    for item in get_all_pairs(market):
        if market == item['market'] and base == item['base'] and quote == item['quote']:
            validate = True
            break
    if validate:
        if amount_to_be_sold > round(get_available_amount_sell(base=base, user_id=current_user.id), 8):
            flash("You don't have enough assets.", "warning")
            return redirect(url_for('portfolio'))
        else:
            asset_price = get_last_price(base=base, quote=quote, market=market)['price']
            amount = round(asset_price * amount_to_be_sold, 8)
            fee = round(amount * default_transaction_fee, 8)
            amount_credit = amount - fee
            # noinspection PyArgumentList
            new_transaction = TransactionsPTCC(
                user_id=current_user.id,
                type="sell",
                market=market,
                base=base,
                quote=quote,
                asset_amount=amount_to_be_sold,
                asset_price=asset_price,
                value=amount,
                fee=fee
            )
            db.session.add(new_transaction)
            db.session.commit()
            update_portfolio_asset = PortfolioAssets.query.filter_by(user_id=current_user.id, asset=base).first()
            update_portfolio_asset.amount = round((update_portfolio_asset.amount - amount_to_be_sold), 8)
            update_portfolio = Portfolio.query.filter_by(user_id=current_user.id).first()
            update_portfolio.wallet = round((update_portfolio.wallet + amount_credit), 8)
            db.session.commit()
            flash(f"Your transaction has been completed.", "success")
            return redirect(url_for('portfolio'))
    else:
        flash("Form didn't validate", "danger")
        return redirect(url_for('portfolio'))


@app.route("/api/account/portfolio/price/<market>/<base>/<quote>/<api_secret>/")
def api_account_portfolio_price(market, base, quote, api_secret):
    if SecureApi().validate(api_secret=api_secret):
        return jsonify(
            get_last_price(base=base, quote=quote, market=market)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/account/portfolio/dropdowns/base/<market>/<api_secret>/")
def api_account_portfolio_dropdown_base(market, api_secret):
    if SecureApi().validate(api_secret=api_secret):
        return jsonify(
            get_pairs_for_portfolio_dropdown(market)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/account/portfolio/dropdowns/quote/<market>/<base>/<api_secret>/")
def api_account_portfolio_dropdown_quote(market, base, api_secret):
    if SecureApi().validate(api_secret=api_secret):
        return jsonify(
            get_quotes_for_portfolio_dropdown(market=market, base=base)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/account/portfolio/update-all/<user_id>/<api_secret>/")
def api_account_portfolio_update_all(user_id, api_secret):
    if SecureApi().validate(api_secret=api_secret, user_id=user_id):
        return jsonify(
            calculate_total_value(user_id=user_id)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/account/portfolio/line-chart/<user_ID>/<days>/<api_secret>/")
def api_account_portfolio_buy_sell_line_chart(user_ID, days, api_secret):
    if SecureApi().validate(api_secret=api_secret, user_id=user_ID):
        return jsonify(
            buy_sell_line_data(user_ID=user_ID, days=days)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/account/portfolio/chart/<delta>/<user_id>/<api_secret>/")
def api_account_portfolio_chart(delta, user_id, api_secret):
    if SecureApi().validate(api_secret=api_secret, user_id=user_id):
        return jsonify(
            portfolio_chart(user_id=user_id, delta=delta)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/account/delete-account/", methods=["GET", "POST"])
@login_required
def delete_account():
    form = AuthorizationForm()
    totp = pyotp.TOTP(current_user.qrcode_secret)
    if form.validate_on_submit():
        if totp.verify(form.pin.data):
            User.query.filter_by(id=current_user.id).delete()
            LoginUser.query.filter_by(user_ID=current_user.id).delete()
            UpdateAuthorizationDetails.query.filter_by(user_id=current_user.id).delete()
            TransactionsPTCC.query.filter_by(user_id=current_user.id).delete()
            Portfolio.query.filter_by(user_id=current_user.id).delete()
            PortfolioAssets.query.filter_by(user_id=current_user.id).delete()
            PortfolioRecord.query.filter_by(user_id=current_user.id).delete()
            MFA.query.filter_by(user_id=current_user.id).delete()
            MFARequests.query.filter_by(user_id=current_user.id).delete()
            Reset2FARequests.query.filter_by(user_id=current_user.id).delete()
            ResetPasswordAuthorizations.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()
            logout_user()
            flash("Your account has been deleted.", "info")
            return redirect(url_for('home'))
        else:
            flash("MFA code was incorrect, please try again.", "danger")
            return redirect(url_for('delete_account'))
    return render_template(
        "delete-account.html",
        form=form,
        title="Delete account"
    )


@app.route("/account/my-data/")
@login_required
def my_data():
    user_info = User.query.filter_by(id=current_user.id).first()
    login_user = LoginUser.query.filter_by(user_ID=current_user.id).order_by(LoginUser.date.desc())
    login_info = []
    for line in login_user:
        login_info.append(
            {
                "date": str(line.date)[:19],
                "IP": line.ipAddress,
                "status": line.status
            }
        )
    transactions_user = TransactionsPTCC.query.filter_by(user_id=current_user.id).order_by(TransactionsPTCC.date_created.desc())
    update_info = UpdateAuthorizationDetails.query.filter_by(user_id=current_user.id).order_by(UpdateAuthorizationDetails.date_created.desc())
    update_info_password = ResetPasswordAuthorizations.query.filter_by(
        user_id=current_user.id).order_by(ResetPasswordAuthorizations.date_created.desc())
    return render_template(
        "data.html",
        title="My data",
        user_info=user_info,
        login_info=login_info,
        transactions_user=transactions_user,
        update_info=update_info,
        update_info_password=update_info_password
    )


@app.route("/account/portfolio/transactions/buy/")
def all_transactions_buy():
    return render_template(
        "portfolio-all-transactions-buy.html",
        title="Account",
        buy_transactions=get_ptcc_transactions(user_ID=current_user.id, type_='buy', limit=None)
    )


@app.route("/account/portfolio/transactions/sell/")
def all_transactions_sell():
    return render_template(
        "portfolio-all-transactions-sell.html",
        title="Account",
        sell_transactions=get_ptcc_transactions(user_ID=current_user.id, type_='sell', limit=None)
    )


@app.route("/about/project/")
def about_project():
    return render_template(
        "about-project.html",
        title="About"
    )


@app.route("/historical-charts/line/")
def historical_charts_line():
    end = datetime.utcnow()
    start = end - timedelta(days=14)
    end += timedelta(days=1)
    return render_template(
        "historical-charts-line.html",
        title="Historical Charts",
        end=str(end)[:10],
        start=str(start)[:10],
        hours=str(start)[11:16],
        candles=candle_options,
    )


@app.route("/historical-charts/ohlc/")
def historical_charts_ohlc():
    end = datetime.utcnow()
    start = end - timedelta(days=14)
    end += timedelta(days=1)
    return render_template(
        "historical-charts-ohlc.html",
        title="Historical Charts",
        end=str(end)[:10],
        start=str(start)[:10],
        hours=str(start)[11:16],
        candles=candle_options,
    )


@app.route("/historical-charts/vtp/")
def historical_charts_vtp():
    end = datetime.utcnow()
    start = end - timedelta(days=14)
    end += timedelta(days=1)
    return render_template(
        "historical-charts-vtp.html",
        title="Historical Charts",
        end=str(end)[:10],
        start=str(start)[:10],
        hours=str(start)[11:16],
        candles=candle_options,
    )


@app.route("/api/historical-charts/line/<base>/<quote>/<market>/<candle>/<api_secret>/")
def api_historical_charts_line_data(base, quote, market, candle, api_secret):
    try:
        candle = int(candle)
    except Exception as e:
        print(e)  # An error log will not be created
        candle = 20
    start = request.args.get('start')
    end = request.args.get('end')
    if SecureApi().validate(api_secret=api_secret):
        return jsonify(
            get_historical_data_line(base=base, quote=quote, market=market, start=start, end=end, candle=candle)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/historical-charts/ohlc/<base>/<quote>/<market>/<candle>/<api_secret>/")
def api_historical_charts_ohlc_data(base, quote, market, candle, api_secret):
    try:
        candle = int(candle)
    except Exception as e:
        print(e)  # An error log will not be created
        candle = 20
    start = request.args.get('start')
    end = request.args.get('end')
    if SecureApi().validate(api_secret=api_secret):
        return jsonify(
            get_historical_data_ohlc(base=base, quote=quote, market=market, start=start, end=end, candle=candle)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/api/historical-charts/vtp/<base>/<quote>/<market>/<candle>/<api_secret>/")
def api_historical_charts_vtp_data(base, quote, market, candle, api_secret):
    try:
        candle = int(candle)
    except Exception as e:
        print(e)  # An error log will not be created
        candle = 20
    start = request.args.get('start')
    end = request.args.get('end')
    if SecureApi().validate(api_secret=api_secret):
        return jsonify(
            get_historical_data_vtp(base=base, quote=quote, market=market, start=start, end=end, candle=candle)
        )
    else:
        return jsonify(
            {}
        )


@app.route("/newsfeed/<page>/<per_page>/")
def newsfeed_page(page, per_page):
    query = request.args.get('query')
    if query is None:
        query = ""
    sources = request.args.get('sources')
    if sources is None:
        sources = ""
    try:
        page = int(page)
    except Exception as e:
        print(e)
        page = 1
    if page <= 0:
        page = 1
    try:
        per_page = int(per_page)
    except Exception as e:
        print(e)
        per_page = default_news_per_page
    if per_page <= 0:
        per_page = default_news_per_page
    total_news = count_all_news(key_words=query, sources=sources)
    if total_news % per_page == 0:
        last_page = total_news // per_page
    else:
        last_page = (total_news // per_page) + 1
    if page > last_page:
        c_page = last_page
    else:
        c_page = page
    return render_template(
        "newsfeed.html",
        title="Newsfeed",
        news=news_search(key_words=query, sources=sources, page=page, per_page=per_page),
        c_page=c_page,
        per_page=per_page,
        last_page=last_page,
        total_news=total_news,
        all_sources=get_all_news_source_id()
    )


@app.route("/competitions/")
def competitions_home():
    if current_user.is_authenticated:
        my_comp = my_competitions(user_id=current_user.id, limit=None)
    else:
        my_comp = []
    return render_template(
        "competitions-home.html",
        title="Competitions",
        my_competitions=my_comp,
        future_competitions=future_competitions(limit=None),
        ongoing_competitions=ongoing_competitions(limit=None)
    )


@app.route("/competitions/<compt_id>/details/")
def competition_details_home(compt_id):
    compt = Competitions.query.filter_by(id=compt_id).first()
    already_in = False
    if compt is None:
        return redirect(url_for("competitions_home"))
    else:
        status = ""
        if compt.start_date < datetime.utcnow() < compt.end_date:
            status = "ongoing"
        elif datetime.utcnow() > compt.end_date:
            status = "past"
        elif compt.start_date > datetime.utcnow():
            status = "future"
        if current_user.is_authenticated:
            filter_ = UsersInCompetitions.query.filter_by(user_id=current_user.id, competition_id=compt.id).first()
            if filter_ is not None:
                already_in = True
        return render_template(
            "competitions-detail.html",
            title="Competitions",
            competition=compt,
            already_in=already_in,
            status=status
        )


@app.route("/competitions/<compt_id>/join/")
@login_required
def competition_join(compt_id):
    compt = Competitions.query.filter_by(id=compt_id).first()
    if compt is None:
        return redirect(url_for("competitions_home"))
    else:
        filter_ = UsersInCompetitions.query.filter_by(user_id=current_user.id, competition_id=compt.id).first()
        if filter_ is not None:
            if compt.start_date < datetime.utcnow() < compt.end_date:
                flash("You cannot join an ongoing competition", "warning")
                return redirect(url_for("competitions_home"))
            elif datetime.utcnow() > compt.end_date:
                flash("This competition has ended", "warning")
                return redirect(url_for("competitions_home"))
            else:
                flash("You are already in the competition!", "info")
                return redirect(url_for("competition_details_home", compt_id=compt_id))
        else:
            if compt.start_date < datetime.utcnow() < compt.end_date:
                flash("You cannot join an ongoing competition", "warning")
                return redirect(url_for("competitions_home"))
            elif datetime.utcnow() > compt.end_date:
                flash("This competition has ended", "warning")
                return redirect(url_for("competitions_home"))
            else:
                # noinspection PyArgumentList
                add = UsersInCompetitions(
                    user_id=current_user.id,
                    competition_id=compt.id
                )
                db.session.add(add)
                # noinspection PyArgumentList
                compt_wallet = CompetitionWallet(
                    user_id=current_user.id,
                    compt_id=compt.id,
                    wallet=compt.start_amount
                )
                db.session.add(compt_wallet)
                for asset_ in default_assets_competitions:
                    # noinspection PyArgumentList
                    compt_asset = CompetitionAssets(
                        user_id=current_user.id,
                        compt_id=compt.id,
                        asset=asset_
                    )
                    db.session.add(compt_asset)
                db.session.commit()
                flash(f"You've joined {compt.name}.", "success")
                return redirect(url_for("competitions_home"))


@app.route("/competitions/<compt_id>/leave/")
@login_required
def competition_leave(compt_id):
    compt = Competitions.query.filter_by(id=compt_id).first()
    if compt is None:
        return redirect(url_for("competitions_home"))
    else:
        if compt.start_date < datetime.utcnow() < compt.end_date:
            flash("You cannot leave an ongoing competition.", "info")
            return redirect(url_for("competitions_home"))
        filter_ = UsersInCompetitions.query.filter_by(user_id=current_user.id, competition_id=compt.id).first()
        if filter_ is None:
            flash("You didn't join this competition yet!", "info")
            return redirect(url_for("competition_details_home", compt_id=compt_id))
        else:
            UsersInCompetitions.query.filter_by(user_id=current_user.id, competition_id=compt.id).delete()
            CompetitionWallet.query.filter_by(user_id=current_user.id, compt_id=compt.id).delete()
            CompetitionAssets.query.filter_by(user_id=current_user.id, compt_id=compt.id).delete()
            db.session.commit()
            flash("You are no longer part in this competition.", "warning")
            return redirect(url_for("competitions_home"))


@app.route("/playground/<compt_id>/live/")
@login_required
def playground_live_home(compt_id):
    compt = Competitions.query.filter_by(id=compt_id).first()
    if compt is None:
        return redirect(url_for("competitions_home"))
    else:
        if compt.start_date < datetime.utcnow() < compt.end_date:
            btc_candle = request.args.get('btc_candle')
            if btc_candle is None:
                btc_candle = default_playground_candle
            else:
                try:
                    btc_candle = int(btc_candle)
                except Exception as e:
                    print(e)  # no error log will be created
                    btc_candle = default_playground_candle
                else:
                    if btc_candle not in candle_values:
                        btc_candle = default_playground_candle
            eth_candle = request.args.get('eth_candle')
            if eth_candle is None:
                eth_candle = default_playground_candle
            else:
                try:
                    eth_candle = int(eth_candle)
                except Exception as e:
                    print(e)  # no error log will be created
                    eth_candle = default_playground_candle
                else:
                    if eth_candle not in candle_values:
                        eth_candle = default_playground_candle
            user_is_in = UsersInCompetitions.query.filter_by(competition_id=compt_id, user_id=current_user.id).first()
            if user_is_in is None:
                # USER IS NOT REGISTERED FOR COMPETITION
                form_buy = None
                form_sell = None
                registered = False
                available_funds = 0
                available_assets = []
                current_value = 0
                var_pct = 0
                transactions = []
            else:
                # USER IS REGISTERED FOR COMPETITION
                form_buy = BuyAssetFormCompetition()
                form_sell = SellAssetFormCompetition()
                registered = True
                available_assets = []
                current_value = 0
                available_funds = CompetitionWallet.query.filter_by(user_id=current_user.id, compt_id=compt.id).first().wallet
                aaa = CompetitionAssets.query.filter_by(user_id=current_user.id, compt_id=compt.id).all()
                for aa in aaa:
                    available_assets.append(
                        {
                            "base": aa.asset,
                            "amount": round(aa.amount, 8)
                        }
                    )
                    last_price = get_last_price(market="kraken", base=aa.asset, quote="eur")['price']
                    current_value += last_price * aa.amount
                current_value += available_funds
                var_pct = round((current_value - compt.start_amount) / compt.start_amount * 100, 3)
                transactions = competitions_transactions(user_id=current_user.id, compt_id=compt_id, limit=5)
            return render_template(
                "playground-home-live.html",
                title="Playground",
                registered=registered,
                btc_candle=btc_candle,
                btc_candle_update=btc_candle // 3,
                eth_candle=eth_candle,
                eth_candle_update=eth_candle // 3,
                compt_id=compt_id,
                form_buy=form_buy,
                form_sell=form_sell,
                available_funds=available_funds,
                available_assets=available_assets,
                current_value=round(current_value, 2),
                var_pct=var_pct,
                buy_fee=compt.buy_fee,
                sell_fee=compt.sell_fee,
                amount_quote=compt.amount_quote,
                days_to_trade=(compt.end_date - datetime.utcnow()).days,
                users_in_compt=UsersInCompetitions.query.filter_by(competition_id=compt.id).count(),
                compt_name=compt.name,
                transactions=transactions
            )
        elif datetime.utcnow() < compt.start_date:
            return redirect(url_for('competitions_home'))
        else:
            return redirect(url_for('playground_home', compt_id=compt_id))


@app.route("/playground/<compt_id>/buy/", methods=["POST"])
@login_required
def playground_live_buy_asset(compt_id):
    compt = Competitions.query.filter_by(id=compt_id).first()
    if compt is None:
        return redirect(url_for("competitions_home"))
    else:
        if compt.start_date < datetime.utcnow() < compt.end_date:
            form = BuyAssetFormCompetition()
            try:
                market = str(form.market.data)
                base = str(form.base.data)
                quote = str(form.quote.data)
                amount_to_be_spent = float(form.amount_spent.data)
            except Exception as e:
                # noinspection PyArgumentList
                error_log = ErrorLogs(
                    route=f'playground live buy asset',
                    log=str(e).replace("'", "")
                )
                db.session.add(error_log)
                db.session.commit()
                flash("Something went wrong, please try again later.", "danger")
                return redirect(url_for("playground_live_home", compt_id=compt_id))
            # CHECK IF USER HAS ENOUGH FUNDS #
            fee_to_be_taken = round(amount_to_be_spent * compt.buy_fee / 100, 2)
            amount_net = round(amount_to_be_spent - fee_to_be_taken, 2)
            last_price = get_last_price(base=base, quote=quote, market=market)["price"]
            asset_to_be_bought = round((amount_to_be_spent - fee_to_be_taken) / last_price, 8)
            line_wallet = CompetitionWallet.query.filter_by(user_id=current_user.id, compt_id=compt_id).first()
            if line_wallet.wallet < amount_to_be_spent:
                flash("There is not enough funds in your wallet", "warning")
                return redirect(url_for("playground_live_home", compt_id=compt_id))
            elif amount_to_be_spent <= 0:
                flash("You need to spend more than that...", "warning")
                return redirect(url_for("playground_live_home", compt_id=compt_id))
            else:
                # noinspection PyArgumentList
                transaction = CompetitionsTransactionsBuy(
                    user_id=current_user.id,
                    compt_id=compt_id,
                    base=base,
                    quote=quote,
                    amount_gross=amount_to_be_spent,
                    fee=fee_to_be_taken,
                    amount_net=amount_net,
                    asset_price=last_price,
                    asset_amount=asset_to_be_bought
                )
                db.session.add(transaction)
                line_asset = CompetitionAssets.query.filter_by(user_id=current_user.id, compt_id=compt_id, asset=base).first()
                line_asset.amount += asset_to_be_bought
                line_wallet.wallet -= amount_to_be_spent
                db.session.commit()
                return redirect(url_for("playground_live_home", compt_id=compt_id))
        else:
            flash("This competition is now closed.", "danger")
            return redirect(url_for("competitions_home"))


@app.route("/playground/<compt_id>/sell/", methods=["POST"])
@login_required
def playground_live_sell_asset(compt_id):
    compt = Competitions.query.filter_by(id=compt_id).first()
    if compt is None:
        return redirect(url_for("competitions_home"))
    else:
        if compt.start_date < datetime.utcnow() < compt.end_date:
            form = SellAssetFormCompetition()
            try:
                market = str(form.market_sell.data)
                base = str(form.base_sell.data)
                quote = str(form.quote_sell.data)
                amount_to_be_sold = float(form.amount_spent_sell.data)
            except Exception as e:
                # noinspection PyArgumentList
                error_log = ErrorLogs(
                    route=f'playground live sell asset',
                    log=str(e).replace("'", "")
                )
                db.session.add(error_log)
                db.session.commit()
                flash("Something went wrong, please try again later.", "danger")
                return redirect(url_for("playground_live_home", compt_id=compt_id))
            # CHECK IF USER HAS ENOUGH FUNDS #
            line_asset = CompetitionAssets.query.filter_by(user_id=current_user.id, compt_id=compt_id, asset=base).first()
            if amount_to_be_sold > line_asset.amount:
                flash("There is not enough funds in your account", "warning")
                return redirect(url_for("playground_live_home", compt_id=compt_id))
            elif amount_to_be_sold <= 0:
                flash("You need to sell more than that...", "warning")
                return redirect(url_for("playground_live_home", compt_id=compt_id))
            else:
                last_price = get_last_price(base=base, quote=quote, market=market)["price"]
                fee = compt.sell_fee
                amount_gross = round(last_price * amount_to_be_sold, 2)
                fee_to_be_taken = round(amount_gross * fee / 100, 2)
                amount_net = amount_gross - fee_to_be_taken
                line_wallet = CompetitionWallet.query.filter_by(user_id=current_user.id, compt_id=compt_id).first()
                # noinspection PyArgumentList
                transaction = CompetitionsTransactionsSell(
                    user_id=current_user.id,
                    compt_id=compt_id,
                    base=base,
                    quote=quote,
                    asset_amount=amount_to_be_sold,
                    asset_price=last_price,
                    amount_gross=amount_gross,
                    fee=fee_to_be_taken,
                    amount_net=amount_net
                )
                db.session.add(transaction)
                line_asset.amount -= amount_to_be_sold
                line_wallet.wallet += amount_net
                db.session.commit()
                return redirect(url_for("playground_live_home", compt_id=compt_id))
        else:
            flash("This competition is now closed.", "danger")
            return redirect(url_for("competitions_home"))


@app.route("/playground/<compt_id>/live/transaction/")
@login_required
def playground_live_transactions(compt_id):
    compt = Competitions.query.filter_by(id=compt_id).first()
    if compt is None:
        return redirect(url_for("competitions_home"))
    else:
        if compt.start_date < datetime.utcnow() < compt.end_date:
            user_is_in = UsersInCompetitions.query.filter_by(competition_id=compt_id, user_id=current_user.id).first()
            if user_is_in is None:
                # USER IS NOT REGISTERED FOR COMPETITION
                form_buy = None
                form_sell = None
                registered = False
                available_funds = 0
                available_assets = []
                current_value = 0
                var_pct = 0
            else:
                # USER IS REGISTERED FOR COMPETITION
                form_buy = BuyAssetFormCompetition()
                form_sell = SellAssetFormCompetition()
                registered = True
                available_assets = []
                current_value = 0
                available_funds = CompetitionWallet.query.filter_by(user_id=current_user.id, compt_id=compt.id).first().wallet
                aaa = CompetitionAssets.query.filter_by(user_id=current_user.id, compt_id=compt.id).all()
                for aa in aaa:
                    available_assets.append(
                        {
                            "base": aa.asset,
                            "amount": round(aa.amount, 8)
                        }
                    )
                    last_price = get_last_price(market="kraken", base=aa.asset, quote="eur")['price']
                    current_value += last_price * aa.amount
                current_value += available_funds
                var_pct = round((current_value - compt.start_amount) / compt.start_amount * 100, 3)
            return render_template(
                "playground-transactions-live.html",
                title="Playground",
                registered=registered,
                compt_id=compt_id,
                form_buy=form_buy,
                form_sell=form_sell,
                available_funds=available_funds,
                available_assets=available_assets,
                current_value=round(current_value, 2),
                var_pct=var_pct,
                buy_fee=compt.buy_fee,
                sell_fee=compt.sell_fee,
                amount_quote=compt.amount_quote,
                days_to_trade=(compt.end_date - datetime.utcnow()).days,
                users_in_compt=UsersInCompetitions.query.filter_by(competition_id=compt.id).count(),
                compt_name=compt.name,
                transactions=competitions_transactions(user_id=None, compt_id=compt_id, limit=50)
            )
        elif datetime.utcnow() < compt.start_date:
            return redirect(url_for('competitions_home'))
        else:
            return redirect(url_for('playground_home', compt_id=compt_id))


@app.route("/playground/<compt_id>/live/hall-of-fame/")
@login_required
def playground_live_hall_of_fame(compt_id):
    compt = Competitions.query.filter_by(id=compt_id).first()
    if compt is None:
        return redirect(url_for("competitions_home"))
    else:
        if compt.start_date < datetime.utcnow() < compt.end_date:
            hall_of_fame = []
            user_is_in = UsersInCompetitions.query.filter_by(competition_id=compt_id, user_id=current_user.id).first()
            all_users = UsersInCompetitions.query.filter_by(competition_id=compt_id).all()
            for user_ in all_users:
                info_port = competition_portfolio_value(user_id=user_.user_id, compt_id=compt_id, full_info=True)
                info_username = User.query.filter_by(id=user_.user_id).first().username
                trans_buy = CompetitionsTransactionsBuy.query.filter_by(user_id=user_.user_id, compt_id=compt_id).count()
                trans_sell = CompetitionsTransactionsSell.query.filter_by(user_id=user_.user_id, compt_id=compt_id).count()
                total_trans = trans_buy + trans_sell
                total_assets = 0
                wallet = 0  # INITIALIZE VARIABLE
                for item in info_port["breakdown"]:
                    if item["asset"] != "wallet":
                        total_assets += item["value"]
                    else:
                        wallet = item["value"]
                hall_of_fame.append(
                    {
                        "info_username": info_username,
                        "info_total_trans": total_trans,
                        "info_total_assets": total_assets,
                        "info_wallet": wallet,
                        "info_current_value": info_port["current_value"],
                        "info_pct_change": info_port["pct_change"],
                    }
                )
            hall_of_fame.sort(key=lambda item: item['info_pct_change'], reverse=True)
            if user_is_in is None:
                # USER IS NOT REGISTERED FOR COMPETITION
                form_buy = None
                form_sell = None
                registered = False
                available_funds = 0
                available_assets = []
                current_value = 0
                var_pct = 0
            else:
                # USER IS REGISTERED FOR COMPETITION
                form_buy = BuyAssetFormCompetition()
                form_sell = SellAssetFormCompetition()
                registered = True
                available_assets = []
                current_value = 0
                available_funds = CompetitionWallet.query.filter_by(user_id=current_user.id, compt_id=compt.id).first().wallet
                aaa = CompetitionAssets.query.filter_by(user_id=current_user.id, compt_id=compt.id).all()
                for aa in aaa:
                    available_assets.append(
                        {
                            "base": aa.asset,
                            "amount": round(aa.amount, 8)
                        }
                    )
                    last_price = get_last_price(market="kraken", base=aa.asset, quote="eur")['price']
                    current_value += last_price * aa.amount
                current_value += available_funds
                var_pct = round((current_value - compt.start_amount) / compt.start_amount * 100, 3)
            return render_template(
                "playground-hall-of-fame-live.html",
                title="Playground",
                registered=registered,
                compt_id=compt_id,
                form_buy=form_buy,
                form_sell=form_sell,
                available_funds=available_funds,
                available_assets=available_assets,
                current_value=round(current_value, 2),
                var_pct=var_pct,
                buy_fee=compt.buy_fee,
                sell_fee=compt.sell_fee,
                amount_quote=compt.amount_quote,
                days_to_trade=(compt.end_date - datetime.utcnow()).days,
                users_in_compt=UsersInCompetitions.query.filter_by(competition_id=compt.id).count(),
                compt_name=compt.name,
                hall_of_fame=hall_of_fame,
                date_=str(datetime.utcnow())[:19]
            )
        elif datetime.utcnow() < compt.start_date:
            return redirect(url_for('competitions_home'))
        else:
            return redirect(url_for('playground_home', compt_id=compt_id))


@app.route("/playground/<compt_id>/")
@login_required
def playground_home(compt_id):
    compt = Competitions.query.filter_by(id=compt_id).first()
    if compt is None:
        return redirect(url_for("competitions_home"))
    else:
        if compt.start_date < datetime.utcnow() < compt.end_date:
            return redirect(url_for('playground_live_home', compt_id=compt_id))
        elif datetime.utcnow() < compt.start_date:
            return redirect(url_for('competitions_home'))
        else:
            # CODE FOR ARCHIVED COMPETITIONS WILL BE HERE
            return render_template(
                "playground-home-archive.html",
                title="Playground",
            )


@app.route("/api/competition/calculate-portfolio/<user_id>/<compt_id>/<api_secret>/")
def api_competition_calculate_portfolio(user_id, compt_id, api_secret):
    if SecureApi().validate(api_secret=api_secret, user_id=user_id, exception=True):
        return jsonify(
            competition_portfolio_value(user_id=user_id, compt_id=compt_id)
        )
    else:
        return jsonify(
            {}
        )
