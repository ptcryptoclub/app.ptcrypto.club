from ptCryptoClub.admin.config import CryptoData
from ptCryptoClub import db
from ptCryptoClub.admin.models import ErrorLogs

from sqlalchemy import create_engine
import pandas as pd

engine_live_data = create_engine(CryptoData.string)


def table_latest_trans(base, quote, market, number_of_trans):
    sql_query = f"""
    select date_created, price, amount from "liveTransactions" lt
        where base = '{base}' and "quote" = '{quote}' and market = '{market}'
        order by date_created DESC
        limit {number_of_trans}
    """
    try:
        data = pd.read_sql_query(sql=sql_query, con=engine_live_data)
    except Exception as e:
        data = pd.DataFrame()
        # noinspection PyArgumentList
        error_log = ErrorLogs(
            route='latest transactions',
            log=str(e).replace("'", "")
        )
        db.session.add(error_log)
        db.session.commit()
    to_return = []
    for i in data.index:
        to_return.append(
            {
                'ind': i + 1,
                'base': base,
                'quote': quote,
                'date': str(data.date_created[i]),
                'price': float(data.price[i]),
                'amount': float(data.amount[i])
            }
        )
    return to_return
