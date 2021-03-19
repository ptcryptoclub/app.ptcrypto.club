from ptCryptoClub.admin.config import CryptoData
from ptCryptoClub import db
from ptCryptoClub.admin.models import ErrorLogs, ApiUsage

from sqlalchemy import create_engine, func
import pandas as pd
import time
from datetime import datetime, timedelta


engine_live_data = create_engine(CryptoData.string)


def admin_main_tables():
    # DATA FROM TRANSACTIONS TABLE #
    query_trans = """
        select  count(*) count,
                min(date_created) min_date,
                max(date_created) max_date
            from public."liveTransactions_2";
    """
    try:
        data_trans = pd.read_sql_query(sql=query_trans, con=engine_live_data)
    except Exception as e:
        data_trans = pd.DataFrame(
            columns=["count", "min_date", "max_date"],
            index=[0]
        )
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='admin functions admin main tables transactions data',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    # DATA FROM 20s OHLC TABLE #
    query_20s = """
            select  count(*) count,
                    min(closetime) min_date,
                    max(closetime) max_date
                from public.ohlc_20s;
        """
    try:
        data_20s = pd.read_sql_query(sql=query_20s, con=engine_live_data)
    except Exception as e:
        data_20s = pd.DataFrame(
            columns=["count", "min_date", "max_date"],
            index=[0]
        )
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='admin functions admin main tables 20s ohlc data',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    # DATA FROM 60s OHLC TABLE #
    query_60s = """
            select  count(*) count,
                    min(closetime) min_date,
                    max(closetime) max_date
                from public.ohlc_60s;
        """
    try:
        data_60s = pd.read_sql_query(sql=query_60s, con=engine_live_data)
    except Exception as e:
        data_60s = pd.DataFrame(
            columns=["count", "min_date", "max_date"],
            index=[0]
        )
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='admin functions admin main tables 60s ohlc data',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    # DATA FROM 300s OHLC TABLE #
    query_300s = """
            select  count(*) count,
                    min(closetime) min_date,
                    max(closetime) max_date
                from public.ohlc_300s;
        """
    try:
        data_300s = pd.read_sql_query(sql=query_300s, con=engine_live_data)
    except Exception as e:
        data_300s = pd.DataFrame(
            columns=["count", "min_date", "max_date"],
            index=[0]
        )
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='admin functions admin main tables 300s ohlc data',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    to_return = {
        "trans_count": data_trans['count'][0],
        "trans_min": data_trans['min_date'][0],
        "trans_max": data_trans['max_date'][0],
        "20s_ohlc_count": data_20s['count'][0],
        "20s_ohlc_min": data_20s['min_date'][0],
        "20s_ohlc_max": data_20s['max_date'][0],
        "60s_ohlc_count": data_60s['count'][0],
        "60s_ohlc_min": data_60s['min_date'][0],
        "60s_ohlc_max": data_60s['max_date'][0],
        "300s_ohlc_count": data_300s['count'][0],
        "300s_ohlc_min": data_300s['min_date'][0],
        "300s_ohlc_max": data_300s['max_date'][0]
    }
    return to_return


def admin_archive_tables():
    # DATA FROM TRANSACTIONS TABLE #
    query_trans = """
        select  count(*) count,
                min(date_created) min_date,
                max(date_created) max_date
            from public."zzTransactionsArquive_1";
    """
    try:
        data_trans = pd.read_sql_query(sql=query_trans, con=engine_live_data)
    except Exception as e:
        data_trans = pd.DataFrame(
            columns=["count", "min_date", "max_date"],
            index=[0]
        )
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='admin functions admin archive tables transactions data',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    # DATA FROM 20s OHLC TABLE #
    query_20s = """
            select  count(*) count,
                    min(closetime) min_date,
                    max(closetime) max_date
                from public."zz_ohlc_20sArquive_1";
        """
    try:
        data_20s = pd.read_sql_query(sql=query_20s, con=engine_live_data)
    except Exception as e:
        data_20s = pd.DataFrame(
            columns=["count", "min_date", "max_date"],
            index=[0]
        )
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='admin functions admin archive tables 20s ohlc data',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    # DATA FROM 60s OHLC TABLE #
    query_60s = """
            select  count(*) count,
                    min(closetime) min_date,
                    max(closetime) max_date
                from public."zz_ohlc_60sArquive_1";
        """
    try:
        data_60s = pd.read_sql_query(sql=query_60s, con=engine_live_data)
    except Exception as e:
        data_60s = pd.DataFrame(
            columns=["count", "min_date", "max_date"],
            index=[0]
        )
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='admin functions admin archive tables 60s ohlc data',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    # DATA FROM 300s OHLC TABLE #
    query_300s = """
            select  count(*) count,
                    min(closetime) min_date,
                    max(closetime) max_date
                from public."zz_ohlc_300sArquive_1";
        """
    try:
        data_300s = pd.read_sql_query(sql=query_300s, con=engine_live_data)
    except Exception as e:
        data_300s = pd.DataFrame(
            columns=["count", "min_date", "max_date"],
            index=[0]
        )
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='admin functions admin archive tables 300s ohlc data',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    to_return = {
        "trans_count": data_trans['count'][0],
        "trans_min": data_trans['min_date'][0],
        "trans_max": data_trans['max_date'][0],
        "20s_ohlc_count": data_20s['count'][0],
        "20s_ohlc_min": data_20s['min_date'][0],
        "20s_ohlc_max": data_20s['max_date'][0],
        "60s_ohlc_count": data_60s['count'][0],
        "60s_ohlc_min": data_60s['min_date'][0],
        "60s_ohlc_max": data_60s['max_date'][0],
        "300s_ohlc_count": data_300s['count'][0],
        "300s_ohlc_min": data_300s['min_date'][0],
        "300s_ohlc_max": data_300s['max_date'][0]
    }
    return to_return


def admin_last_update():
    query = """
    select 	updated as updated,
            base as base,
            "quote" as "quote",
            market as market
        from lastupdate l;
    """
    try:
        data = pd.read_sql_query(sql=query, con=engine_live_data)
    except Exception as e:
        data = pd.DataFrame(
            columns=["updated", "base", "quote", "market"]
        )
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='admin functions admin last update',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    to_return = []
    for i in data.index:
        delta = int((pd.to_datetime(time.time(), unit="s") - data['updated'][i]).total_seconds())
        if delta < 60:
            all_good = True
        else:
            all_good = False
        to_return.append(
            {
                "market": data.market[i],
                "base": data.base[i],
                "quote": data.quote[i],
                "date": str(data['updated'][i])[:19],
                "all_good": all_good
            }
        )
    return to_return


def admin_api_usage_data():
    t = datetime.utcnow() - timedelta(hours=24)
    t = t.replace(second=0, microsecond=0, minute=0)
    to_return = []
    raw_data = db.session.query(func.sum(ApiUsage.usage), ApiUsage.date).filter(ApiUsage.date >= t).order_by(ApiUsage.date).group_by(ApiUsage.date).all()
    for i in raw_data:
        to_return.append(
            {
                "date": str(i[1])[:19],
                "usage": int(i[0])
            }
        )
    return to_return
