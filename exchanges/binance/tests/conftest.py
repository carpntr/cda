import pytest
import requests
import vcr
import json
import pytz
from datetime import datetime as dt

@pytest.fixture
@vcr.use_cassette('exchanges/binance/tests/cassettes/get-depth.yml')
def depth_call():
    url = 'https://www.binance.com/api/v1/depth?symbol=BNBBTC'
    resp = requests.get(url)
    resp_dict = json.loads(resp.content)
    return resp_dict

@pytest.fixture
def depth_update():
    new_vals = {'e': 'depthUpdate',
                'E': 1708956388669,
                'b': [
                    ['', '0.0000', []]
                ],
                'a': [
                    ['', '69.00', []]
                ],
                'u': 1
                }
    return new_vals

@pytest.fixture
def timestamp():
    return
