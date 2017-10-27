import vcr
from exchanges.binance.client import create_url, DepthSocket

def test_create_url():
    protocol = 'https'
    host = 'www.binance.com'
    base_path = '/api/v1/depth'
    params = {'symbol': 'BNBBTC'}
    expected_url = 'https://www.binance.com/api/v1/depth?symbol=BNBBTC'
    url = create_url(protocol, host, base_path, params)
    assert url == expected_url



@vcr.use_cassette('exchanges/binance/tests/cassettes/get-depth.yml')
def test_initialize_book():
    """
    This case is pretty well covered in test_book, but we can redo it here
    """
    depth_socket = DepthSocket('BNBBTC', fetch_base=False)
    assert depth_socket.initialize_book() == 200

    # This one is not though!
    @vcr.use_cassette('exchanges/binance/tests/cassettes/get-depth-fail.yml')
    def bad_resp():
        bad_socket = DepthSocket('BADTICKER', fetch_base=False)
        resp = bad_socket.initialize_book()
        return resp
    assert bad_resp() == 400


