from ptCryptoClub.admin.config import CryptoData
from ptCryptoClub.admin.models import LivePairs
from ptCryptoClub.admin.sql.card_functions import last_price, price_change, max_min, volume

from sqlalchemy import create_engine

engine_live_data = create_engine(CryptoData.string)


def get_all_markets():
    all_markets = []
    query = LivePairs.query.with_entities(LivePairs.market).distinct()
    for result in query:
        all_markets.append(result.market)
    return all_markets


def get_all_pairs(market):
    all_pairs = []
    query = LivePairs.query.filter_by(market=market, in_use=True).with_entities(LivePairs.base, LivePairs.quote).distinct()
    for result in query:
        all_pairs.append(
            {
                'base': result[0],
                'quote': result[1],
                'market': market
            }
        )
    return all_pairs


def card_generic(base, quote, market, delta):
    maximum, minimum = max_min(base, quote, market, delta)
    sum_base, sum_quote = volume(base, quote, market, delta)
    to_return = {
        'base': base,
        'quote': quote,
        'market': market,
        'change': price_change(base, quote, market, delta),
        'last_price': last_price(base, quote, market),
        'high': maximum,
        'low': minimum,
        'volume': int(sum_base),
        'volume_quote': int(sum_quote)
    }
    return to_return
