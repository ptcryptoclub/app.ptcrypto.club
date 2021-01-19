from ptCryptoClub.admin.config import CryptoData
from ptCryptoClub.admin.models import LivePairs
from ptCryptoClub.admin.sql.card_functions import last_price, price_change, max_min, volume
from ptCryptoClub.admin.sql.latest_transactions import table_latest_trans
from ptCryptoClub.admin.models import ErrorLogs
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
    maximum, minimum = max_min(base, quote, market, delta)
    sum_base, sum_quote = volume(base, quote, market, delta)
    change = price_change(base, quote, market, delta)
    price = last_price(base, quote, market)
    to_return = {
        'base': base,
        'quote': quote,
        'market': market,
        'change': change,
        'last_price': price,
        'high': maximum,
        'low': minimum,
        'volume': int(sum_base),
        'volume_quote': int(sum_quote),
        'delta': delta
    }
    return to_return


def table_latest_transactions(base, quote, market, number_of_trans):
    return table_latest_trans(base, quote, market, number_of_trans)
