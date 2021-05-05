from ptCryptoClub.admin.config import CryptoData, qr_code_folder, admins_emails
from ptCryptoClub import db
from ptCryptoClub.admin.models import User, LoginUser, UpdateAuthorizationDetails, ErrorLogs, TransactionsPTCC, Portfolio, PortfolioAssets, ApiUsage

from sqlalchemy import create_engine, func
import pandas as pd
import time
from datetime import datetime, timedelta
import os


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
    # DATA FROM 900s OHLC TABLE #
    query_900s = """
            select  count(*) count,
                    min(closetime) min_date,
                    max(closetime) max_date
                from public.ohlc_900s;
        """
    try:
        data_900s = pd.read_sql_query(sql=query_900s, con=engine_live_data)
    except Exception as e:
        data_900s = pd.DataFrame(
            columns=["count", "min_date", "max_date"],
            index=[0]
        )
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='admin functions admin main tables 900s ohlc data',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    # DATA FROM 1800s OHLC TABLE #
    query_1800s = """
            select  count(*) count,
                    min(closetime) min_date,
                    max(closetime) max_date
                from public.ohlc_1800s;
        """
    try:
        data_1800s = pd.read_sql_query(sql=query_1800s, con=engine_live_data)
    except Exception as e:
        data_1800s = pd.DataFrame(
            columns=["count", "min_date", "max_date"],
            index=[0]
        )
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='admin functions admin main tables 1800s ohlc data',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    # DATA FROM 3600s OHLC TABLE #
    query_3600s = """
            select  count(*) count,
                    min(closetime) min_date,
                    max(closetime) max_date
                from public.ohlc_3600s;
        """
    try:
        data_3600s = pd.read_sql_query(sql=query_3600s, con=engine_live_data)
    except Exception as e:
        data_3600s = pd.DataFrame(
            columns=["count", "min_date", "max_date"],
            index=[0]
        )
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='admin functions admin main tables 3600s ohlc data',
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
        "300s_ohlc_max": data_300s['max_date'][0],
        "900s_ohlc_count": data_900s['count'][0],
        "900s_ohlc_min": data_900s['min_date'][0],
        "900s_ohlc_max": data_900s['max_date'][0],
        "1800s_ohlc_count": data_1800s['count'][0],
        "1800s_ohlc_min": data_1800s['min_date'][0],
        "1800s_ohlc_max": data_1800s['max_date'][0],
        "3600s_ohlc_count": data_3600s['count'][0],
        "3600s_ohlc_min": data_3600s['min_date'][0],
        "3600s_ohlc_max": data_3600s['max_date'][0]
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


def admin_api_details():
    try:
        not_user = User.query.filter_by(username="notUser").first()
        t = datetime.utcnow()
        td30 = (t - timedelta(days=30)).replace(second=0, microsecond=0, minute=0)
        td7 = (t - timedelta(days=7)).replace(second=0, microsecond=0, minute=0)
        th24 = (t - timedelta(hours=24)).replace(second=0, microsecond=0, minute=0)
        base = db.session.query(func.sum(ApiUsage.usage))
        to_return = {
            "total": int(
                base.scalar()
            ),
            "total_users": int(
                base.filter(ApiUsage.user_id != not_user.id).scalar()
            ),
            "total_n_users": int(
                base.filter(ApiUsage.user_id == not_user.id).scalar()
            ),
            "last_month": int(
                base.filter(ApiUsage.date >= td30).scalar()
            ),
            "last_month_users": int(
                base.filter(ApiUsage.date >= td30, ApiUsage.user_id != not_user.id).scalar()
            ),
            "last_month_n_users": int(
                base.filter(ApiUsage.date >= td30, ApiUsage.user_id == not_user.id).scalar()
            ),
            "last_week": int(
                base.filter(ApiUsage.date >= td7).scalar()
            ),
            "last_week_users": int(
                base.filter(ApiUsage.date >= td7, ApiUsage.user_id != not_user.id).scalar()
            ),
            "last_week_n_users": int(
                base.filter(ApiUsage.date >= td7, ApiUsage.user_id == not_user.id).scalar()
            ),
            "last_24h": int(
                base.filter(ApiUsage.date >= th24).scalar()
            ),
            "last_24h_users": int(
                base.filter(ApiUsage.date >= th24, ApiUsage.user_id != not_user.id).scalar()
            ),
            "last_24h_n_users": int(
                base.filter(ApiUsage.date >= th24, ApiUsage.user_id == not_user.id).scalar()
            ),
        }
    except Exception as e:
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='admin functions admin api details',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
        to_return = {
            "total": "na",
            "total_users": "-",
            "total_n_users": "-",
            "last_month": "na",
            "last_month_users": "-",
            "last_month_n_users": "-",
            "last_week": "na",
            "last_week_users": "-",
            "last_week_n_users": "-",
            "last_24h": "na",
            "last_24h_users": "-",
            "last_24h_n_users": "-",
        }
    return to_return


def admin_api_usage_top_5():
    tm = (datetime.utcnow() - timedelta(hours=24)).replace(second=0, microsecond=0, minute=0)
    data = db.session.query(func.sum(ApiUsage.usage), ApiUsage.user_id).filter(ApiUsage.date >= tm).group_by(ApiUsage.user_id).limit(5).all()
    to_return = []
    for t in data:
        to_return.append(
            {
                'usage': int(t[0]),
                'user_id': int(t[1])
            }
        )
    return to_return


def admin_users_data_sample():
    to_return = []
    data = User.query.order_by(User.date.desc()).limit(5)
    for user in data:
        to_return.append(
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'account_type': user.account_type,
                'active': user.active,
                'date': str(user.date)[:10]
            }
        )
    return to_return


def admin_users_data(page):
    per_page = 5
    total_users = User.query.count()
    if total_users % per_page == 0:
        last_page = total_users // per_page
    else:
        last_page = (total_users // per_page) + 1
    try:
        page = int(page)
        if page <= 0:
            page = 1
    except Exception as e:
        page = 1
        print(e)  # an error log will not be created
    if page > last_page:
        page = last_page
    start = (page - 1) * per_page
    end = start + per_page
    to_return = []
    data = User.query.order_by(User.id.asc()).slice(start, end)
    for user in data:
        to_return.append(
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'account_type': user.account_type,
                'active': user.active,
                'date': str(user.date)[:10]
            }
        )
    return to_return, page, last_page


def admin_delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user.email in admins_emails or user.username == "notUser":
        return None
    else:
        if user.qrcode_img is not None:
            if os.path.exists(qr_code_folder+str(user.qrcode_img)+".png"):
                os.remove(qr_code_folder+str(user.qrcode_img)+".png")
        User.query.filter_by(id=user_id).delete()
        LoginUser.query.filter_by(user_ID=user_id).delete()
        UpdateAuthorizationDetails.query.filter_by(user_id=user_id).delete()
        TransactionsPTCC.query.filter_by(user_id=user_id).delete()
        Portfolio.query.filter_by(user_id=user_id).delete()
        PortfolioAssets.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        return None
