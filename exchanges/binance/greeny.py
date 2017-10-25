from gevent import monkey
monkey.patch_all()
import websocket
import ssl
import requests
import json
import gevent
from urllib.parse import urlencode


def create_url(protocol, host, base_path, params):
    """Build request url"""
    params = ("?" + urlencode(params)) if params else ""
    url = f'{protocol}://{host}{base_path}'
    return url + params


class BinanceWebSocket:
    ws_protocol = 'wss'
    ws_host = 'stream.binance.com'
    ws_port = '9443'
    ws_base_path = '/ws'

    def __init__(self, callback, api_key=None):
        self.api_key = api_key
        self.callback = callback
        self.ws = None
        self.ssl_opt = {"cert_reqs": ssl.CERT_NONE}

    def _on_message(self, ws, message):
        data = json.loads(message)
        self.callback(data)

    def _on_error(self, ws, error):
        raise Exception(error)


class DepthSocket(BinanceWebSocket):
    # Should probably move these attributes to a RESTConfig/WSConfig class?
    rest_protocol = 'https'
    rest_host = 'www.binance.com'
    rest_base_path = '/api/v1/depth'

    def __init__(self, symbol, callback, fetch_base=True):
        super().__init__(callback)
        self.symbol = symbol
        self.params = {'symbol': symbol}
        self.bids = {}
        self.asks = {}
        if fetch_base:
            self.initialize_book()


    def initialize_book(self):
        """Get depth for self.symbol"""
        rest_url = create_url(self.rest_protocol, self.rest_host,
                              self.rest_base_path, self.params)
        resp = requests.get(rest_url)
        depth = json.loads(resp.content)

        # Initialize bid/ask data
        self.last_update_id = depth['lastUpdateId']
        self.bids = {k: v for k, v, _ in depth['bids']}
        self.asks = {k: v for k, v, _ in depth['asks']}
        return resp.status_code


    def update_book(self, new_values):
        """Update state of the book"""
        if new_values['lastUpdateId'] > self.last_update_id:
            self.last_update_id = new_values['lastUpdateId']
            new_bids = {k: v for k, v, _ in new_values['bids']}
            new_asks = {k: v for k, v, _ in new_values['asks']}
            for k, v in new_bids.items():
                self.bids[k] = v
                if v == '0.00000000':
                    del self.bids[k]
            for k, v in new_asks.items():
                self.asks[k] = v
                if v == '0.00000000':
                    del self.asks[k]
            return self.bids, self.asks, self.last_update_id
        else:
            pass

    def stream(self):
        call_path = f'/{self.symbol.lower()}@depth'
        url = f'{self.ws_protocol}://{self.ws_host}:{self.ws_port}{self.ws_base_path}{call_path}'
        self.ws = websocket.WebSocketApp(url,
                                         on_message=self._on_message,
                                         on_error=self._on_error)
        self.ws.run_forever(sslopt=self.ssl_opt)

class OrderBook:
    """Collection of depth tickers?"""
    def __init__(self, symbols, api_key=None):
        self.api_key = api_key
        self.symbols = symbols
        self.state = None
        self.book = {}

    def _on_update(self, msg):
        """Specify what to do with new data"""
        print(msg)
        gevent.sleep(0)

    def stream_orderbook(self):
        bucket = self.symbols
        def hatch(sym):
            sock = DepthSocket(symbol=sym, callback=self._on_update)
            sock.stream()
        threads = [gevent.spawn(hatch, sym) for sym in bucket]
        gevent.joinall(threads)

if __name__ == '__main__':
    # api_key = '3GaVoDlAmF0graxcPJcN4MmMpBTgvadi0XshjQZWvY57DbEgDxBt9Jf6ELTlOjB9'
    # q = BinanceWebSocket(symbol='BNBBTC', api_key=api_key)
    # q.stream()
    q = OrderBook(symbols=['BNBBTC', 'ETHBTC'])
    q.stream_orderbook()
