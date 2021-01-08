from ptCryptoClub.admin.config import CryptoData
from ptCryptoClub import db
from ptCryptoClub.admin.models import ErrorLogs

from sqlalchemy import create_engine
import pandas as pd

engine_live_data = create_engine(CryptoData.string)


def last_price(base, quote, market):
    sql_query = f"""
    select price from "livePrice" lp
        where base = '{base}' and "quote" = '{quote}' and market = '{market}'
        order by date_created desc
        limit 1
    """
    try:
        data = pd.read_sql_query(sql=sql_query, con=engine_live_data)
        last_price = float(data.price[0])
    except Exception as e:
        last_price = None
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='card functions last price',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    return last_price


def price_change(base, quote, market, delta):
    sql_query = f"""
    select * from "livePrice" lp
	where date_created in 
	(
		select date_created from "livePrice" lp
			where date_created >= now() - interval '{delta} minute' and base = '{base}' and "quote" = '{quote}' and market = '{market}'
			order by date_created
			limit 1
	)
	or date_created in
	(
		select date_created from "livePrice" lp
			where base = '{base}' and "quote" = '{quote}' and market = '{market}'
			order by date_created desc
			limit 1
	)
	order by date_created asc
    """
    try:
        data = pd.read_sql_query(sql=sql_query, con=engine_live_data)
        data = data.loc[(data.base == base) & (data.quote == quote) & (data.market == market)].reset_index()
        price_change = float(round(data.price.pct_change()[1] * 100, 2))
    except Exception as e:
        price_change = None
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='card functions price change',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    return price_change


def max_min(base, quote, market, delta):
    sql_query = f"""
    select 	max(highprice),
            min(lowprice)
        from "liveOHLC"
        where closetime >= now() - interval '{delta} minute' and base = '{base}' and "quote" = '{quote}' and market = '{market}'
    """
    try:
        data = pd.read_sql_query(sql=sql_query, con=engine_live_data)
        maximum = float(data['max'][0])
        minimum = float(data['min'][0])
    except Exception as e:
        maximum = None
        minimum = None
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='card functions max min',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    return maximum, minimum


def volume(base, quote, market, delta):
    sql_query = f"""
    select base, "quote", sum(amount) sum_base, sum(price * amount) sum_quote from "liveTransactions"
        where date_created >= now() - interval '{delta} minute' and base = '{base}' and "quote" = '{quote}' and market = '{market}'
        group by base, "quote"
    """
    try:
        data = pd.read_sql_query(sql=sql_query, con=engine_live_data)
        sum_base = float(data.sum_base[0])
        sum_quote = float(data.sum_quote[0])
    except Exception as e:
        sum_base = None
        sum_quote = None
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='card functions volume',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    return sum_base, sum_quote


"""print(price_change('btc', 'eur', 'kraken', 180))
print(max_min('btc', 'eur', 'kraken', 180))
print(last_price('btc', 'eur', 'kraken'))
print(volume('btc', 'eur', 'kraken', 180))"""
