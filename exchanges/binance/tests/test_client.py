import vcr
import requests
import json
from exchanges.binance.client import DepthSocket, create_url

def test_create_url():
    protocol = 'https'
    host = 'www.binance.com'
    base_path = '/api/v1/depth'
    params = {'symbol': 'BNBBTC'}
    expected_url = 'https://www.binance.com/api/v1/depth?symbol=BNBBTC'
    url = create_url(protocol, host, base_path, params)
    assert url == expected_url

depth = DepthSocket('BNBBTC', False)
@vcr.use_cassette('exchanges/binance/tests/cassettes/get-depth.yml')
def test_initialize_book():
    ret_code = depth.initialize_book()
    assert ret_code == 200

    # need better cases here
    assert isinstance(depth.bids, dict) and len(depth.bids) > 0

def test_update_book():
    # Set some arbitrary values
    depth.bids['1'] = '3'
    depth.bids['2'] = '4'
    new_vals = {'e':'depthUpdate',
                'E': 1508956388669,
                'b': [['1', '2.123', []],
                         ['2', '0.00000000', []]
                         ],
                'a': [['69', '5', []]],
                'u': depth.last_update_id + 1
                }
    depth.update_book(new_vals)
    assert depth.bids['1'] == new_vals['b'][0][1]
    assert '2' not in depth.bids
    assert '69' in depth.asks
    depth.update_book({'b':[], 'E': 1508956388669, 'a': [], 'u': depth.last_update_id + 1})

