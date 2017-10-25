import vcr
import json
import pprint
from exchanges.binance.client import Depth


depth = Depth('BNBBTC', False)
def test_create_url():
    expected_url = 'https://www.binance.com/api/v1/depth?symbol='
    assert depth.create_url() == expected_url+depth.symbol

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
    new_vals = {'bids': [['1', '2.123', []],
                         ['2', '0.00000000', []]
                         ],
                'asks': [['69', '5', []]],
                'lastUpdateId': depth.last_update_id + 1
                }
    depth.update_book(new_vals)
    assert depth.bids['1'] == new_vals['bids'][0][1]
    assert '2' not in depth.bids
    assert '69' in depth.asks
    depth.update_book({'bids':[], 'asks': [], 'lastUpdateId': depth.last_update_id + 1})

