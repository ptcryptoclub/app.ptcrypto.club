from ptCryptoClub.admin.config import CryptoData
from ptCryptoClub import db
from ptCryptoClub.admin.models import ErrorLogs

from sqlalchemy import create_engine
import pandas as pd
import time

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
