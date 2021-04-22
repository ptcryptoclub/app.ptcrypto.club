from ptCryptoClub.admin.config import CryptoData
from ptCryptoClub import db
from ptCryptoClub.admin.models import ErrorLogs

from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime, timedelta

engine_live_data = create_engine(CryptoData.string)


def ohlc_chart_data(base, quote, market, datapoints, candle):
    query = f"""
    select t.*
        from (
            select 	closetime,
                    openprice,
                    highprice,
                    lowprice,
                    closeprice,
                    volume
                from public.ohlc_{str(candle)}s os
                where base = '{base}' and "quote" = '{quote}' and market = '{market}'
                order by closetime desc
                limit {str(datapoints)}
        ) as t
        order by t.closetime asc
    """
    try:
        data = pd.read_sql_query(sql=query, con=engine_live_data)
        data['moving_avg'] = data.closeprice.rolling(12, min_periods=1).mean()
        # data['moving_exp'] = data.closeprice.rolling(4, min_periods=1).mean()
        data['moving_exp'] = data.closeprice.ewm(com=4).mean()
    except Exception as e:
        data = pd.DataFrame(
            columns=["closetime", "openprice", "highprice", "lowprice", "closeprice", "volume", "volumequote", "moving_avg", "moving_exp"]
        )
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='ohlc functions 20s data',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    to_return = []
    for i in data.index:
        to_return.append(
            {
                "closetime": str(data.closetime[i])[:19],
                "openprice": data.openprice[i],
                "highprice": data.highprice[i],
                "lowprice": data.lowprice[i],
                "closeprice": data.closeprice[i],
                "volume": data.volume[i],
                "moving_avg": data.moving_avg[i],
                "moving_exp": data.moving_exp[i]
            }
        )
    return to_return


def line_chart_data(base, quote, market, last_x_hours):
    query = f"""
    select 	closetime,
            closeprice
        from public.ohlc_20s os
        where closetime >= now() - interval '{str(last_x_hours)} hour' and base = '{base}' and "quote" = '{quote}' and market = '{market}'
        order by closetime asc
    """
    try:
        data = pd.read_sql_query(sql=query, con=engine_live_data)
    except Exception as e:
        data = pd.DataFrame(columns=["closetime", "openprice", "highprice", "lowprice", "closeprice", "volume", "volumequote"])
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='ohlc functions 20s data',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    to_return = []
    for i in data.index:
        to_return.append(
            {
                "date": str(data.closetime[i])[:19],
                "closeValue": data.closeprice[i]
            }
        )
    return to_return


def vtp_chart_data(base, quote, market, datapoints, candle):
    query = f"""
    select t.*
        from (
        
            select 	closetime,
                    "nTrans",
                    "maxVolume",
                    volume - "maxVolume" volume,
                    "maxVolumePrice",
                    closeprice
                from ohlc_{str(candle)}s os
                where base = '{base}' and "quote" = '{quote}' and market = '{market}'
                order by closetime desc
                limit {str(datapoints)}
        ) as t
        order by t.closetime asc
    """
    try:
        data = pd.read_sql_query(sql=query, con=engine_live_data)
    except Exception as e:
        data = pd.DataFrame(
            columns=["closetime", "nTrans", "maxVolume", "volume", "maxVolumePrice", "closeprice"]
        )
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='ohlc functions 20s data',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    to_return = []
    for i in data.index:
        to_return.append(
            {
                "closetime": str(data.closetime[i])[:19],
                "nTrans": int(data.nTrans[i]),
                "maxVolume": float(data.maxVolume[i]),
                "volume": float(data.volume[i]),
                "maxVolumePrice": float(data.maxVolumePrice[i]),
                "closeprice": float(data.closeprice[i])
            }
        )
    return to_return


def get_historical_data_line(base: str, quote: str, market: str, start=None, end=None, candle=None):
    default_delta_20 = 8
    default_delta_60 = 24
    default_delta_300 = 120
    if candle is None:
        candle = 20
    if candle not in [20, 60, 300]:
        candle = 20
    if start is None and end is None:
        if candle == 20:
            end = datetime.utcnow()
            start = end - timedelta(hours=default_delta_20)
        elif candle == 60:
            end = datetime.utcnow()
            start = end - timedelta(hours=default_delta_60)
        else:
            end = datetime.utcnow()
            start = end - timedelta(hours=default_delta_300)
    elif start is None:
        try:
            end = pd.to_datetime(end)
        except Exception as e:
            print(e) # An error log will not be created
            end = datetime.utcnow()
        else:
            end = pd.to_datetime(end)
        if candle == 20:
            start = end - timedelta(hours=default_delta_20)
        elif candle == 60:
            start = end - timedelta(hours=default_delta_60)
        else:
            start = end - timedelta(hours=default_delta_300)
    elif end is None:
        try:
            start = pd.to_datetime(start)
        except Exception as e:
            print(e)  # An error log will not be created
            return get_historical_data_line(base=base, quote=quote, market=market, start=None, end=None, candle=candle)
        if candle == 20:
            end = start + timedelta(hours=default_delta_20)
        elif candle == 60:
            end = start + timedelta(hours=default_delta_60)
        else:
            end = start + timedelta(hours=default_delta_300)
    else:
        try:
            start = pd.to_datetime(start)
        except Exception as e:
            print(e)  # An error log will not be created
            return get_historical_data_line(base=base, quote=quote, market=market, start=None, end=end, candle=candle)
        try:
            end = pd.to_datetime(end)
        except Exception as e:
            print(e)  # An error log will not be created
            return get_historical_data_line(base=base, quote=quote, market=market, start=start, end=None, candle=candle)
    query_1 = f"""
        select  closetime,
                closeprice
            from public.ohlc_{candle}s
            where base='{base}' and quote='{quote}' and market='{market}'
                and closetime between '{start}' and '{end}'
            order by closetime asc
    """
    data_1 = pd.read_sql_query(sql=query_1, con=engine_live_data)
    query_2 = f"""
        select  closetime,
                closeprice
            from public."zz_ohlc_{candle}sArquive_1"
                where base='{base}' and quote='{quote}' and market='{market}'
                    and closetime between '{start}' and '{end}'
                order by closetime asc
    """
    data_2 = pd.read_sql_query(sql=query_2, con=engine_live_data)
    data = pd.concat([data_1, data_2])
    data = data.sort_values('closetime').reset_index(drop=True)
    to_return = []
    for i in data.index:
        to_return.append(
            {
                "date": str(data.closetime[i])[:19],
                "closeprice": data.closeprice[i]
            }
        )
    return to_return


def get_historical_data_ohlc(base: str, quote: str, market: str, start=None, end=None, candle=None):
    default_delta_20 = 8
    default_delta_60 = 24
    default_delta_300 = 120
    if candle is None:
        candle = 20
    if candle not in [20, 60, 300]:
        candle = 20
    if start is None and end is None:
        if candle == 20:
            end = datetime.utcnow()
            start = end - timedelta(hours=default_delta_20)
        elif candle == 60:
            end = datetime.utcnow()
            start = end - timedelta(hours=default_delta_60)
        else:
            end = datetime.utcnow()
            start = end - timedelta(hours=default_delta_300)
    elif start is None:
        try:
            end = pd.to_datetime(end)
        except Exception as e:
            print(e) # An error log will not be created
            end = datetime.utcnow()
        else:
            end = pd.to_datetime(end)
        if candle == 20:
            start = end - timedelta(hours=default_delta_20)
        elif candle == 60:
            start = end - timedelta(hours=default_delta_60)
        else:
            start = end - timedelta(hours=default_delta_300)
    elif end is None:
        try:
            start = pd.to_datetime(start)
        except Exception as e:
            print(e) # An error log will not be created
            return get_historical_data_ohlc(base=base, quote=quote, market=market, start=None, end=None, candle=candle)
        if candle == 20:
            end = start + timedelta(hours=default_delta_20)
        elif candle == 60:
            end = start + timedelta(hours=default_delta_60)
        else:
            end = start + timedelta(hours=default_delta_300)
    else:
        try:
            start = pd.to_datetime(start)
        except Exception as e:
            print(e) # An error log will not be created
            return get_historical_data_ohlc(base=base, quote=quote, market=market, start=None, end=end, candle=candle)
        try:
            end = pd.to_datetime(end)
        except Exception as e:
            print(e) # An error log will not be created
            return get_historical_data_ohlc(base=base, quote=quote, market=market, start=start, end=None, candle=candle)
    query_1 = f"""
        select  closetime,
                openprice,
                highprice,
                lowprice,
                closeprice,
                volume
            from public.ohlc_{candle}s
            where base='{base}' and quote='{quote}' and market='{market}'
                and closetime between '{start}' and '{end}'
            order by closetime asc
    """
    data_1 = pd.read_sql_query(sql=query_1, con=engine_live_data)
    query_2 = f"""
        select  closetime,
                openprice,
                highprice,
                lowprice,
                closeprice,
                volume
            from public."zz_ohlc_{candle}sArquive_1"
            where base='{base}' and quote='{quote}' and market='{market}'
                and closetime between '{start}' and '{end}'
            order by closetime asc
    """
    data_2 = pd.read_sql_query(sql=query_2, con=engine_live_data)
    data = pd.concat([data_1, data_2])
    data = data.sort_values('closetime').reset_index(drop=True)
    to_return = []
    for i in data.index:
        to_return.append(
            {
                "closetime": str(data.closetime[i])[:19],
                "openprice": data.openprice[i],
                "highprice": data.highprice[i],
                "lowprice": data.lowprice[i],
                "closeprice": data.closeprice[i],
                "volume": data.volume[i]
            }
        )
    return to_return


def get_historical_data_vtp(base: str, quote: str, market: str, start=None, end=None, candle=None):
    default_delta_20 = 8
    default_delta_60 = 24
    default_delta_300 = 120
    if candle is None:
        candle = 20
    if candle not in [20, 60, 300]:
        candle = 20
    if start is None and end is None:
        if candle == 20:
            end = datetime.utcnow()
            start = end - timedelta(hours=default_delta_20)
        elif candle == 60:
            end = datetime.utcnow()
            start = end - timedelta(hours=default_delta_60)
        else:
            end = datetime.utcnow()
            start = end - timedelta(hours=default_delta_300)
    elif start is None:
        try:
            end = pd.to_datetime(end)
        except Exception as e:
            print(e) # An error log will not be created
            end = datetime.utcnow()
        else:
            end = pd.to_datetime(end)
        if candle == 20:
            start = end - timedelta(hours=default_delta_20)
        elif candle == 60:
            start = end - timedelta(hours=default_delta_60)
        else:
            start = end - timedelta(hours=default_delta_300)
    elif end is None:
        try:
            start = pd.to_datetime(start)
        except Exception as e:
            print(e) # An error log will not be created
            return get_historical_data_vtp(base=base, quote=quote, market=market, start=None, end=None, candle=candle)
        if candle == 20:
            end = start + timedelta(hours=default_delta_20)
        elif candle == 60:
            end = start + timedelta(hours=default_delta_60)
        else:
            end = start + timedelta(hours=default_delta_300)
    else:
        try:
            start = pd.to_datetime(start)
        except Exception as e:
            print(e) # An error log will not be created
            return get_historical_data_vtp(base=base, quote=quote, market=market, start=None, end=end, candle=candle)
        try:
            end = pd.to_datetime(end)
        except Exception as e:
            print(e) # An error log will not be created
            return get_historical_data_vtp(base=base, quote=quote, market=market, start=start, end=None, candle=candle)
    query_1 = f"""
        select  closetime,
                "nTrans",
                "maxVolume",
                volume - "maxVolume" volume,
                "maxVolumePrice",
                closeprice
            from public.ohlc_{candle}s
            where base='{base}' and quote='{quote}' and market='{market}'
                and closetime between '{start}' and '{end}'
            order by closetime asc
    """
    data_1 = pd.read_sql_query(sql=query_1, con=engine_live_data)
    query_2 = f"""
        select  closetime,
                "nTrans",
                "maxVolume",
                volume - "maxVolume" volume,
                "maxVolumePrice",
                closeprice
            from public."zz_ohlc_{candle}sArquive_1"
            where base='{base}' and quote='{quote}' and market='{market}'
                and closetime between '{start}' and '{end}'
            order by closetime asc
    """
    data_2 = pd.read_sql_query(sql=query_2, con=engine_live_data)
    data = pd.concat([data_1, data_2])
    data = data.sort_values('closetime').reset_index(drop=True)
    to_return = []
    for i in data.index:
        to_return.append(
            {
                "closetime": str(data.closetime[i])[:19],
                "nTrans": int(data.nTrans[i]),
                "maxVolume": float(data.maxVolume[i]),
                "volume": float(data.volume[i]),
                "maxVolumePrice": float(data.maxVolumePrice[i]),
                "closeprice": float(data.closeprice[i])
            }
        )
    return to_return
