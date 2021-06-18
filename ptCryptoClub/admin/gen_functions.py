from ptCryptoClub.admin.config import CryptoData, admins_emails, default_delta, default_fiat, BlockEmail
from ptCryptoClub.admin.sql.latest_transactions import table_latest_trans
from ptCryptoClub.admin.models import User, ErrorLogs, TransactionsPTCC, Portfolio, PortfolioAssets, ApiUsage, IpAddressLog, PortfolioRecord
from ptCryptoClub import db

from sqlalchemy import create_engine
from flask import request
import pandas as pd
import random
import string
from datetime import datetime, timedelta
import time
import requests

engine_live_data = create_engine(CryptoData.string)
engine_web_app = None


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


def get_all_fiats():
    query = """
    select distinct(symbol) as fiat
	    from public.fiatprices2
    """
    try:
        data = pd.read_sql_query(sql=query, con=engine_live_data)
    except Exception as e:
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='generic functions get all fiats',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
        data = pd.DataFrame(columns=["fiat"])
    all_fiats = []
    for fiat in data.fiat:
        all_fiats.append(fiat)
    return all_fiats


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
    assets_details = {}
    for asset in assets:
        last_price = get_last_price(market=market, base=asset.asset, quote=quote)['price']
        assets_value += last_price * asset.amount
        value = last_price * asset.amount
        assets_details.update(
            {
                asset.asset: round(value, 2)
            }
        )
    total = wallet_value.wallet + assets_value
    percentage = round(((total - wallet_value.start) / wallet_value.start) * 100, 1)
    return {
        'value': round(total, 2),
        'wallet': round(wallet_value.wallet, 2),
        'assets': round(assets_value, 2),
        'assets_details': assets_details,
        'percentage': percentage,
        'quote': quote
    }


class SecureApi:
    def __init__(self):
        pass

    def validate(self, api_secret, user_id=None, admin=None, exception=False):
        self.log_ip()
        if exception:
            pass
        else:
            if request.headers.get('Cookie') is None or request.headers.get('Referer') is None:
                return False
        if admin is not None:
            user = User.query.filter_by(api_secret=api_secret).first()
            if user is not None:
                if user.email in admins_emails:
                    self.increment(user.id)
                    return True
                else:
                    return False
            else:
                return False
        else:
            if user_id is None:
                user = User.query.filter_by(api_secret=api_secret).first()
            else:
                user = User.query.filter_by(api_secret=api_secret, id=user_id).first()
        if user is not None:
            self.increment(user.id)
            return True
        else:
            return False

    def get_api_secret(self, user_id):
        if user_id is None:
            api_secret = User.query.filter_by(username="notUser").first().api_secret
        else:
            api_secret = User.query.filter_by(id=user_id).first().api_secret
        return api_secret

    def increment(self, user_id):
        date = hour_rounder(datetime.utcnow())
        api_usage_line = ApiUsage.query.filter_by(user_id=user_id, date=date).first()
        if api_usage_line is None:
            # noinspection PyArgumentList
            new_line = ApiUsage(
                user_id=user_id,
                date=date,
                usage=1
            )
            db.session.add(new_line)
            db.session.commit()
        else:
            api_usage_line.usage += 1
            db.session.commit()
        return None

    def log_ip(self):
        ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        date = hour_rounder(datetime.utcnow())
        ip_log_line = IpAddressLog.query.filter_by(ip_address=ip_address, date=date).first()
        if ip_log_line is None:
            # noinspection PyArgumentList
            ip_line = IpAddressLog(
                ip_address=ip_address,
                date=date,
            )
            db.session.add(ip_line)
            db.session.commit()
        else:
            pass


def buy_sell_line_data(user_ID, days):
    query = f"""
    select 	"type",
            to_timestamp(floor((extract('epoch' from date_created) / 86400 )) * 86400) AT TIME ZONE 'UTC' as "date",
            sum(value) as total
        from "transactionsPTCC" tp 
        where user_id = {user_ID} 
            and date_created >= (select to_timestamp(floor((extract('epoch' from now() - interval '{days} day') / {days} )) * {days}) AT TIME ZONE 'UTC') 
        group by "date", "type"
    """
    try:
        data = db.engine.execute(query)
    except Exception as e:
        data = []
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='generic functions buy sell line data',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    to_df = [row for row in data]
    df = pd.DataFrame(to_df, columns=["type", "date", "total"])
    to_return = []
    for i in df.loc[df.type == "buy"].index:
        to_return.append(
            {
                "date": df['date'][i],
                "total_buy": round(float(df['total'][i]), 2)
            }
        )
    for i in df.loc[df.type == "sell"].index:
        control = True
        for j in to_return:
            if j['date'] == df['date'][i]:
                j['total_sell'] = round(float(df['total'][i]), 2)
                control = False
        if control:
            to_return.append(
                {
                    "date": df['date'][i],
                    "total_sell": round(float(df['total'][i]), 2)
                }
            )
    to_return.sort(key=lambda item: item['date'], reverse=False)
    for item in to_return:
        item['date'] = str(item['date'])
    return to_return


def hash_generator(LENGTH):
    base = string.digits + string.digits + string.ascii_letters
    hash = "".join(random.choice(base) for _ in range(LENGTH))
    return hash


def get_data_live_chart(market, base, quote, data_points, delta):
    query = f"""
    select *
        from (
            select  closetime,
                    "nTrans"
                from ohlc_{delta}s os
                where base = '{base}' and "quote" = '{quote}' and market = '{market}'
                order by closetime desc
                limit {data_points}
        ) as t
        order by closetime asc
    """
    try:
        data = pd.read_sql_query(sql=query, con=engine_live_data)
    except Exception as e:
        data = pd.DataFrame(columns=["closetime", "nTrans"])
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='generic functions get data live chart',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    to_return = []
    for i in data.index:
        to_return.append(
            {
                "closetime": str(data['closetime'][i])[:19],
                "nTrans": int(data['nTrans'][i])
            }
        )
    return to_return


def get_price(market, base_1, base_2, quote, data_points):
    query = f"""
        select 	tb."date",
                tb.price1,
                tb2.price2
            from (
                select 	closetime as "date",
                        closeprice as price1
                    from public.ohlc_20s os
                    where os.market = '{market}' and os.base = '{base_1}' and os."quote" = '{quote}'
                    order by os.closetime desc
                    limit {data_points}
            ) as tb
            join (
                select 	closetime as "date",
                        closeprice as price2
                    from public.ohlc_20s os2
                    where os2.market = '{market}' and os2.base = '{base_2}' and os2."quote" = '{quote}'
                    order by os2.closetime desc
                    limit {data_points}
            ) as tb2
                on tb."date" = tb2."date"
            order by tb."date" asc;
    """
    try:
        data = pd.read_sql_query(sql=query, con=engine_live_data)
    except Exception as e:
        data = pd.DataFrame(columns=["date", "price1", "price2"])
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='generic functions get price',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    to_return = []
    for i in data.index:
        to_return.append(
            {
                "date": str(data["date"][i])[:19],
                "price1": float(data["price1"][i]),
                "price2": float(data["price2"][i])
            }
        )
    return to_return


def hour_rounder(t):
    return t.replace(second=0, microsecond=0, minute=0)


def cci(market_1, base_1, quote_1, market_2, base_2, quote_2, delta: int, starting_point=None):
    if starting_point is None:
        query = f"""
            select 	table_1."date" as "closedate",
            		table_1.crypto_1,
            		table_2.crypto_2
            	from (
            		select 	closetime as "date",
            				closeprice as "crypto_1"
            			from ohlc_20s os1
            			where market = '{market_1}' and base = '{base_1}' and "quote" = '{quote_1}'
            			order by os1.closetime desc
            	) as table_1
            	join (
            		select 	closetime as "date",
            				closeprice as "crypto_2"
            			from ohlc_20s os1
            			where market = '{market_2}' and base = '{base_2}' and "quote" = '{quote_2}'
            			order by os1.closetime desc
            	) as table_2
            	on table_1."date" = table_2."date"
            	where table_1."date" >= (now() - interval '{delta} minute')::timestamp
            	order by table_1."date" asc;
            """
    else:
        query = f"""
        select 	table_1."date" as "closedate",
                table_1.crypto_1,
                table_2.crypto_2
            from (
                select 	closetime as "date",
                        closeprice as "crypto_1"
                    from ohlc_20s os1
                    where market = '{market_1}' and base = '{base_1}' and "quote" = '{quote_1}'
                    order by os1.closetime desc
            ) as table_1
            join (
                select 	closetime as "date",
                        closeprice as "crypto_2"
                    from ohlc_20s os1
                    where market = '{market_2}' and base = '{base_2}' and "quote" = '{quote_2}'
                    order by os1.closetime desc
            ) as table_2
            on table_1."date" = table_2."date"
            where table_1."date" >= ('{starting_point}'::timestamp - interval '{delta} minute')::timestamp
            order by table_1."date" asc;
        """
    try:
        data = pd.read_sql_query(sql=query, con=engine_live_data)
        index = data.corr().iloc[0, 1]
        index = abs(index)
    except Exception as e:
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route=f'generic functions cci {market_1}, {base_1}, {quote_1}, {market_2}, {base_2}, {quote_2}',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
        index = 0
    return {'cci': index}


def cci_chart(market_1, base_1, quote_1, market_2, base_2, quote_2, datapoints: int):
    start = int(time.time())
    delta = 15 * 60  # in seconds
    list_of_times = []
    for i in range(datapoints):
        list_of_times.append(str(pd.to_datetime(start - i * delta, unit='s'))[:19])
    list_of_times.reverse()
    to_return = []
    for time_ in list_of_times:
        to_return.append(
            {
                'date': time_,
                'cci': round(cci(market_1, base_1, quote_1, market_2, base_2, quote_2, 60, starting_point=time_)['cci'], 4)
            }
        )
    return to_return


def gen_fiats(delta=None):
    if delta is None:
        delta = default_delta
    try:
        delta = int(delta)
    except Exception as e:
        delta = default_delta
        print(e)  # An error log will not be created
    delta = delta // 60
    query = f"""
    select 	table1.symbol as symbol,
            table1.exchange as price,
            round(((table1.exchange - table2.exchange)/table2.exchange*100)::numeric, 3) as "change"-- this is already as a percentage 
        from (
            select	exchange,
                    symbol,
                    date_created 
                from fiatprices2 f 
                where date_created in (
                    select max(date_created) from fiatprices2 f2
                    )
        ) as table1
        join (
            select	exchange,
                    symbol,
                    date_created 
                from fiatprices2 f 
                where date_created in (
                    select distinct (date_created)
                        from fiatprices2 f2
                        order by date_created desc
                    limit 1 offset {delta}
                    )
        ) as table2
        on table1.symbol = table2.symbol
        order by symbol
    """
    try:
        data = pd.read_sql_query(sql=query, con=engine_live_data)
    except Exception as e:
        data = pd.DataFrame()
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route=f'generic functions gen fiats',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    to_return = []
    for i in data.index:
        to_return.append(
            {
                "symbol": data['symbol'][i],
                "price": data['price'][i],
                "change": data['change'][i]
            }
        )
    return to_return


def fiat_line_chart_data(fiat, delta=None):
    if delta is None:
        delta = 24
    try:
        delta = int(delta)
    except Exception as e:
        print(e)
        delta = default_delta
    try:
        fiat = fiat.upper()
    except Exception as e:
        print(e)
        fiat = default_fiat
    if fiat not in get_all_fiats():
        fiat = default_fiat
    query = f"""
    select 	DATE_TRUNC('hour', table1.date_created) as "date",
            table1.price
        from (
            select 	date_created,
                    exchange as price
                from fiatprices2 f
                where f.symbol = '{fiat}' and date_created >= (now() - interval '{delta} hour')::timestamp
                order by date_created desc
        ) as table1
        order by date_created asc
    """
    try:
        data = pd.read_sql_query(sql=query, con=engine_live_data)
    except Exception as e:
        data = pd.DataFrame()
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route=f'generic functions fiat line chart data',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    to_return = []
    for i in data.index:
        to_return.append(
            {
                'date': str(data['date'][i]),
                'price': float(data['price'][i])
            }
        )
    return to_return


def get_fiat_name(fiat):
    query = f"""
    select "name" from public.fiatdescription where symbol = '{fiat}'
    """
    try:
        data = pd.read_sql_query(sql=query, con=engine_live_data)
    except Exception as e:
        data = pd.DataFrame()
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route=f'generic functions get fiat name',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    if data.shape[0] > 0:
        name = data['name'][0]
    else:
        name = None
    return name


def email_validation_disposable_emails(email):
    url = f"https://block-temporary-email.com/check/email/{email}"
    headers = {'x-api-key': BlockEmail.access_token}
    message = 'Valid email'
    try:
        data = requests.get(url=url, headers=headers).json()
    except Exception as e:
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route=f'generic functions email validation disposable email',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
        return True, message
    if data['status'] == 200:
        if data['temporary']:
            return False, 'Please use a non disposable email'
        else:
            if data['dns']:
                return True, message
            else:
                return False, 'Please provide a valid email address'
    else:
        return True, message


def newsfeed(n):
    try:
        n = int(n)
    except Exception as e:
        print(e)
        n = 25
    query = f"""
    select 	title,
            url,
            img,
            date_created 
        from public.newsfeed order by random() limit {n};
    """
    try:
        data = pd.read_sql_query(sql=query, con=engine_live_data)
    except Exception as e:
        data = pd.DataFrame()
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route=f'newsfeed',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    to_return = []
    cut = 78
    for i in data.index:
        title = data.title[i]
        if len(title) >= cut:
            title = title[:cut] + " ..."
        else:
            pass
        to_return.append(
            {
                "title": title,
                "url": data.url[i],
                "img": data.img[i],
                "date": str(data.date_created[i])
            }
        )
    return to_return


def count_all_news(key_words: str, sources: str = ""):
    key_words = " ".join(key_words.split())  # this will remove any extra spaces
    key_list = key_words.split(" ")
    key_list = [f"'%%{word}%%'" for word in key_list]
    title = " and title ilike ".join(key_list)
    body = " and body ilike ".join(key_list)
    query_1 = f"""
            select count(*) as count_
                from newsfeed nf
                where ((title ilike {title}) or (body ilike {body}))
                    and (source_id ilike '%%{sources}%%')
    """
    query_2 = f"""
                select count(*) as count_
                    from "zz_newsfeedArquive1" nfa
                    where ((title ilike {title}) or (body ilike {body}))
                        and (source_id ilike '%%{sources}%%')
        """
    try:
        data_1 = pd.read_sql_query(sql=query_1, con=engine_live_data)
        data_2 = pd.read_sql_query(sql=query_2, con=engine_live_data)
    except Exception as e:
        data_1 = pd.DataFrame(columns=["count_"])
        data_2 = pd.DataFrame(columns=["count_"])
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route=f'newsfeed',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    if data_1.shape[0] > 0:
        number_1 = data_1["count_"][0]
    else:
        number_1 = 0
    if data_2.shape[0] > 0:
        number_2 = data_2["count_"][0]
    else:
        number_2 = 0
    return number_1 + number_2


def get_all_news_source_id():
    to_return = []
    query = """
        select source_id
            from (
                select distinct source_id from newsfeed n
                union
                select distinct source_id from "zz_newsfeedArquive1" zna
            ) as t1
            order by t1.source_id asc;
    """
    try:
        data = pd.read_sql_query(sql=query, con=engine_live_data)
    except Exception as e:
        data = pd.DataFrame(columns=["source_id"])
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route=f'get all news source id',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    for i in data.index:
        to_return.append(
            {
                "source_id": data["source_id"][i]
            }
        )
    return to_return


def news_search(key_words: str, sources: str = "", page: int = 1, per_page: int = 12):
    key_words = " ".join(key_words.split())  # this will remove any extra spaces
    key_list = key_words.split(" ")
    key_list = [f"'%%{word}%%'" for word in key_list]
    title = " and title ilike ".join(key_list)
    body = " and body ilike ".join(key_list)
    query = f"""
        select  ROW_NUMBER () OVER (ORDER BY date_created desc) as id,
                news_id,
                date_created,
                source_id,
                title,
                body,
                url,
                img 
            from (
                select 	news_id,
                        date_created,
                        source_id,
                        title,
                        body,
                        url,
                        img
                    from "zz_newsfeedArquive1" zna
                    where ((title ilike {title}) or (body ilike {body}))
                        and (source_id ilike '%%{sources}%%')
                union
                select 	news_id,
                        date_created,
                        source_id,
                        title,
                        body,
                        url,
                        img
                    from newsfeed n
                    where ((title ilike {title}) or (body ilike {body}))
                        and (source_id ilike '%%{sources}%%')
            ) as aaa
            order by date_created desc
            limit {per_page} offset {(page - 1) * per_page};
    """
    try:
        data = pd.read_sql_query(sql=query, con=engine_live_data)
    except Exception as e:
        data = pd.DataFrame()
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route=f'news search',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    to_return = []
    for i in data.index:
        to_return.append(
            {
                "id": data['id'][i],
                "news_id": data['news_id'][i],
                "source_id": data['source_id'][i],
                "date": str(data['date_created'][i])[:19],
                "title": data['title'][i],
                "body": data['body'][i],
                "url": data['url'][i],
                "img": data['img'][i]
            }
        )
    return to_return


def portfolio_chart(user_id, delta=30):
    if delta == "full":
        data = PortfolioRecord.query.filter(PortfolioRecord.user_id == user_id).all()
    else:
        try:
            delta = int(delta)
        except Exception as e:
            print(e)
            delta = 30
        data = PortfolioRecord.query.filter(
            PortfolioRecord.user_id == user_id,
            PortfolioRecord.date_created >= datetime.utcnow() - timedelta(days=delta)
        ).all()
    to_return = []
    for i in range(len(data)):
        to_return.append(
            {
                "date": str(data[i].date_created)[:19],
                "value": data[i].value,
                "wallet": data[i].wallet,
                "assets": data[i].assets,
                "percentage": data[i].percentage
            }
        )
    return to_return


def portfolio_data_start_info(user_id: int):
    try:
        max_ = PortfolioRecord.query.with_entities(
            PortfolioRecord.value).filter_by(user_id=user_id).order_by(PortfolioRecord.value.desc()).first()[0]
    except Exception as e:
        print(e)
        max_ = 0
    try:
        min_ = PortfolioRecord.query.with_entities(
            PortfolioRecord.value).filter_by(user_id=user_id).order_by(PortfolioRecord.value.asc()).first()[0]
    except Exception as e:
        print(e)
        min_ = 0
    try:
        start_ = Portfolio.query.filter_by(user_id=user_id).first().start
    except Exception as e:
        print(e)
        start_ = 0
    data_full = [
        {
            "name": "Min",
            "value": min_
        },
        {
            "name": "Max",
            "value": max_
        },
        {
            "name": "Start",
            "value": start_
        }]
    return data_full


def portfolio_rank_table():
    # get all users from database
    users = User.query.filter_by(active=True)

    to_return = []
    for user in users:
        wallet_value = Portfolio.query.filter_by(user_id=user.id).first()
        data = calculate_total_value(user_id=user.id, market='kraken', quote='eur')
        pct_assets = round(data["assets"]/data["value"]*100)
        pct_fiat = round(data["wallet"] / data["value"] * 100)
        data.update(
            {
                "username": user.username,
                "amount": wallet_value.start,
                "date": str(user.date_active)[:10],
                "pct_assets": pct_assets,
                "pct_fiat": pct_fiat
            }
        )
        to_return.append(
            data
        )
    to_return = sorted(to_return, key=lambda k: k['percentage'], reverse=True)
    return to_return


