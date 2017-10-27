import vcr
import pytest
import pytz
from datetime import datetime as dt
from exchanges.binance.order_book import OrderBook
from util.exceptions import *


book = OrderBook()


def test_initialize_book(depth_call):
    # Case 1: Invalid depth_dict
    bad_dict = {'key': 'value'}
    with pytest.raises(expected_exception=InvalidOrderBook):
        book.initialize(bad_dict)

    # Case 2: Valid depth_dict
    book.initialize(depth_call)
    assert book.bids and book.asks and book.last_update_id is not None


def test_update_book(depth_call, depth_update):
    # Case 1: Set some arbitrary values
    book.initialize(depth_call)
    bid_0, ask_0 = list(book.bids.keys())[0], list(book.asks.keys())[0]
    ask_1 = list(book.asks.keys())[1]
    new_vals = depth_update
    new_vals['b'][0][0] = bid_0
    new_vals['a'][0][0] = ask_0
    new_vals['a'][1][0] = ask_1
    new_vals['u'] = book.last_update_id
    book.update(new_vals)
    assert bid_0 not in book.bids
    assert book.asks[ask_0] == '69.00'
    assert ask_1 not in book.asks


    # Case 2: No update id
    new_vals.pop('u')
    with pytest.raises(expected_exception=InvalidOrderBook):
        book.update(new_vals)

    # Case 3: Invalid update key
    new_vals['e'] = 'wrongUpdate'
    with pytest.raises(expected_exception=InvalidOrderBook):
        book.update(new_vals)


def test_dump(timestamp):
    book.timestamp = 2000.0
    book.last_update_id = 71
    book.bids = {'1': '2', '3': '4'}
    book.asks = {'4': '2', '5': '4'}

    # Arctic dump -- WOW pandas sucks at orderbooks
    ad_exp = [{'index': dt.fromtimestamp(2, tz=pytz.timezone('US/Eastern')),
               'depth_id': book.last_update_id,
               'bid1': '3', 'bid1_ammt': '4', 'bid2': '1', 'bid2_ammt': '2',
               'ask1': '4', 'ask1_ammt': '2', 'ask2': '5', 'ask2_ammt': '4'
               }]
    assert book.dump(style='arctic') == ad_exp

    # Document dump
    assert book.dump() == {'id': book.last_update_id,
                           'timestamp': book.timestamp,
                           'bids': book.bids, 'asks': book.asks}



