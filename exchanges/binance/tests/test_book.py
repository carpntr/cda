from exchanges.binance.order_book import OrderBook
import vcr
import requests
import json


book = OrderBook()

@vcr.use_cassette('exchanges/binance/tests/cassettes/get-depth.yml')
def test_initialize_book():
    url = 'https://www.binance.com/api/v1/depth?symbol=BNBBTC'
    resp = requests.get(url)
    assert resp.status_code == 200
    depth_dict = json.loads(resp.content)
    book.initialize(depth_dict)
    assert isinstance(book.bids, dict) and len(book.bids) > 0


def test_update_book():
    # Set some arbitrary values
    bid_before = list(book.bids.keys())[0]
    ask_before = list(book.asks.keys())[0]
    new_vals = {'e':'depthUpdate',
                'E': 1708956388669,
                'b': [
                    [bid_before, '0.0000', []]
                ],
                'a': [
                    [ask_before, '69.00', []]
                ],
                'u': book.last_update_id + 1
                }
    book.update(new_vals)
    assert bid_before not in book.bids
    assert book.asks[ask_before] == '69.00'


