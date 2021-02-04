from ptCryptoClub.admin.config import CryptoData
from ptCryptoClub.admin.sql.latest_transactions import table_latest_trans
from ptCryptoClub.admin.models import User, ErrorLogs, TransactionsPTCC, Portfolio, PortfolioAssets
from ptCryptoClub import db

from sqlalchemy import create_engine
import pandas as pd

engine_live_data = create_engine(CryptoData.string)


def get_all_markets():
    query = """
    select distinct(market) as market
	    from public.live_pairs lp
    """
    try:
        data = pd.read_sql_query(sql=query, con=engine_live_data)
    except Exception as e:
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='generic functions get all markets',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
        data = pd.DataFrame(columns=["market"])
    all_markets = []
    for market in data.market:
        all_markets.append(market)
    return all_markets


def get_all_pairs(market):
    query = f"""
    select 	distinct(base) as base,
            "quote",
            market
        from public.live_pairs lp
        where quote in (
            select distinct("quote") as pair
                from public.live_pairs lp
                where market = '{market}'
        )
        and in_use is true
    """
    try:
        data = pd.read_sql_query(sql=query, con=engine_live_data)
    except Exception as e:
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route=f'generic functions get all pairs for {market}',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
        data = pd.DataFrame(columns=["base", "quote", "market"])
    all_pairs = []
    for i in data.index:
        all_pairs.append(
            {
                'base': data.base[i],
                'quote': data.quote[i],
                'market': market
            }
        )
    return all_pairs


def card_generic(base, quote, market, delta):
    query = f"""
    SELECT base, "quote", market, "change", price, high, low, volume, volumequote
        FROM public."infoCards"
        where base = '{base}' and quote = '{quote}' and market = '{market}' and delta = {str(delta)};
    """
    try:
        data = pd.read_sql_query(sql=query, con=engine_live_data)
    except Exception as e:
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route=f'generic functions card generic for {base}, {quote} and {market}',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
        data = pd.DataFrame(columns=["base", "quote", "market", "change", "price", "high", "low", "volume", "volumequote"])
    to_return = {
        'base': data.base[0],
        'quote': data.quote[0],
        'market': data.market[0],
        'change': float(data.change[0]),
        'last_price': float(data.price[0]),
        'high': float(data.high[0]),
        'low': float(data.low[0]),
        'volume': int(data.volume[0]),
        'volume_quote': int(data.volumequote[0]),
        'delta': int(delta)
    }
    return to_return


def table_latest_transactions(base, quote, market, number_of_trans):
    return table_latest_trans(base, quote, market, number_of_trans)


def hide_ip(ip):
    hidden_ip = ""
    length = len(ip) - 4
    for i, char in enumerate(ip):
        if i == 0 or i > length:
            hidden_ip += char
        else:
            hidden_ip += "*"
    return hidden_ip


def get_last_price(base, quote, market):
    query = f"""
        SELECT price
            FROM public."infoCards"
            where base = '{base}' and quote = '{quote}' and market = '{market}' and delta = 60;
        """
    try:
        data = pd.read_sql_query(sql=query, con=engine_live_data)
    except Exception as e:
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route=f'generic functions get last price for {base}, {quote} and {market}',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
        data = pd.DataFrame(columns=["price"])
    to_return = {
        'price': float(data.price[0])
    }
    return to_return


def get_pairs_for_portfolio_dropdown(market):
    query = f"""
        select distinct (base) as base
            from public.live_pairs lp
            where market = '{market}' and in_use is true
    """
    try:
        data = pd.read_sql_query(sql=query, con=engine_live_data)
    except Exception as e:
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route=f'generic functions get pairs for portfolio dropdown - {market}',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
        data = pd.DataFrame(columns=["base"])
    to_return = [{'base': ''}]
    for base in data.base:
        to_return.append(
            {
                'base': base
            }
        )
    return to_return


def get_quotes_for_portfolio_dropdown(market, base):
    query = f"""
        select distinct (quote) as quote
            from public.live_pairs lp
            where market = '{market}' and base = '{base}' and in_use is true
    """
    try:
        data = pd.read_sql_query(sql=query, con=engine_live_data)
    except Exception as e:
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route=f'generic functions get quotes for portfolio dropdown - {market} and {base}',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
        data = pd.DataFrame(columns=["quote"])
    to_return = [{'quote': ''}]
    for quote in data.quote:
        to_return.append(
            {
                'quote': quote
            }
        )
    return to_return


def get_available_amount(user_id):
    amount = Portfolio.query.filter_by(user_id=user_id).first()
    return round(amount.wallet, 2)


def get_available_amount_sell(base, user_id):
    line = PortfolioAssets.query.filter_by(user_id=user_id, asset=base).first()
    return line.amount


def get_available_assets(user_id):
    port = PortfolioAssets.query.filter_by(user_id=user_id)
    assets = []
    for line in port:
        assets.append(
            {
                'base': line.asset,
                'amount': round(line.amount, 8)
            }
        )
    return assets


def get_ptcc_transactions(user_ID, type_, limit):
    if limit is None:
        transactions = TransactionsPTCC.query.filter_by(user_id=user_ID, type=type_).order_by(TransactionsPTCC.date_created.desc())
    else:
        transactions = TransactionsPTCC.query.filter_by(user_id=user_ID, type=type_).order_by(TransactionsPTCC.date_created.desc()).limit(limit)
    to_return = []
    for transaction in transactions:
        to_return.append(
            {
                'date': str(transaction.date_created)[:19],
                'type': transaction.type,
                'market': transaction.market,
                'base': transaction.base,
                'quote': transaction.quote,
                'value': round(transaction.value, 8),
                'fee': round(transaction.fee, 8),
                'asset_price': round(transaction.asset_price, 8),
                'asset_amount': round(transaction.asset_amount, 8),
            }
        )
    return to_return


def calculate_total_value(user_id, market='kraken', quote='eur'):
    wallet_value = Portfolio.query.filter_by(user_id=user_id).first()
    assets = PortfolioAssets.query.filter_by(user_id=user_id)
    assets_value = 0
    for asset in assets:
        last_price = get_last_price(market=market, base=asset.asset, quote=quote)['price']
        assets_value += last_price * asset.amount
    total = wallet_value.wallet + assets_value
    percentage = round(((total - wallet_value.start) / wallet_value.start)*100, 1)
    return {
        'value': round(total, 2),
        'wallet': round(wallet_value.wallet, 2),
        'assets': round(assets_value, 2),
        'percentage': percentage,
        'quote': quote
    }


class SecureApi:
    def __init__(self):
        pass

    def validate(self, api_secret):
        user = User.query.filter_by(api_secret=api_secret).first()
        if user is not None:
            return True
        else:
            return False

    def get_api_secret(self, user_id):
        if user_id is None:
            api_secret = User.query.filter_by(username="notUser").first().api_secret
        else:
            api_secret = User.query.filter_by(id=user_id).first().api_secret
        return api_secret
