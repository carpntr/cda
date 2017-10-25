from gevent import monkey
monkey.patch_all()
import websocket
import ssl
import requests
import json
import gevent
from urllib.parse import urlencode


class BinanceWebSocket:
    protocol = 'wss'
    host = 'stream.binance.com'
    port = '9443'
    base_path = '/ws'

    def __init__(self, symbol, callback, api_key=None):
        self.symbol = symbol
        self.api_key = api_key
        self.callback = callback
        self.ws = None
        self.ssl_opt = {"cert_reqs": ssl.CERT_NONE}

    def _on_message(self, ws, message):
        data = json.loads(message)
        self.callback(data)

    def _on_error(self, ws, error):
        raise Exception(error)

    def stream(self):
        call_path = f'/{self.symbol.lower()}@depth'
        url = f'{self.protocol}://{self.host}:{self.port}{self.base_path}{call_path}'
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

    def _on_update(values):
        print(values)
        gevent.sleep(0)

    def stream_orderbook(self):
        def hatch(sym):
            sock = BinanceWebSocket(symbol=sym, api_key=self.api_key,
                                    callback=self._on_update)
            sock.stream()
        bucket = self.symbols
        threads = [gevent.spawn(hatch, sym) for sym in bucket]
        gevent.joinall(threads)


class Depth:
    protocol = 'https'
    host = 'www.binance.com'
    base_path = '/api/v1/depth'

    def __init__(self, symbol, fetch_base=True):
        self.symbol = symbol
        self.url = None
        self.create_url()
        self.bids = {}
        self.asks = {}
        if fetch_base:
            self.initialize_book()


    def initialize_book(self):
        """Get depth for self.symbol"""
        resp = requests.get(self.url)
        depth = json.loads(resp.content)
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


    def create_url(self):
        """Build request url"""
        self.url = f'{self.protocol}://{self.host}{self.base_path}?symbol={self.symbol}'
        return self.url



if __name__ == '__main__':
    # api_key = '3GaVoDlAmF0graxcPJcN4MmMpBTgvadi0XshjQZWvY57DbEgDxBt9Jf6ELTlOjB9'
    # q = BinanceWebSocket(symbol='BNBBTC', api_key=api_key)
    # q.stream()
    q = OrderBook(symbols=['BNBBTC', 'ETHBTC'])
    q.stream_orderbook()