import vcr
import requests
import json
from exchanges.binance.client import create_url

def test_create_url():
    protocol = 'https'
    host = 'www.binance.com'
    base_path = '/api/v1/depth'
    params = {'symbol': 'BNBBTC'}
    expected_url = 'https://www.binance.com/api/v1/depth?symbol=BNBBTC'
    url = create_url(protocol, host, base_path, params)
    assert url == expected_url


