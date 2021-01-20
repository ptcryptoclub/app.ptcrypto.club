from ptCryptoClub.admin.config import CryptoData
from ptCryptoClub import db
from ptCryptoClub.admin.models import ErrorLogs

from sqlalchemy import create_engine
import pandas as pd

engine_live_data = create_engine(CryptoData.string)


def ohlc_chart_data(base, quote, market, last_x_hours):
    query = f"""
    select 	closetime,
            openprice,
            highprice,
            lowprice,
            closeprice,
            volume,
            volumequote
        from public.ohlc_20s os
        where closetime >= now() - interval '{str(last_x_hours)} hour' and base = '{base}' and "quote" = '{quote}' and market = '{market}'
        order by closetime asc
    """
    try:
        data = pd.read_sql_query(sql=query, con=engine_live_data)
        data['pct_change'] = data.closeprice.pct_change()
        data['pct_change'] = data['pct_change'].fillna(0)
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
                "closetime": str(data.closetime[i])[:19],
                "openprice": data.openprice[i],
                "highprice": data.highprice[i],
                "lowprice": data.lowprice[i],
                "closeprice": data.closeprice[i],
                "volume": data.volume[i],
                "rel_change": data['pct_change'][i]
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
