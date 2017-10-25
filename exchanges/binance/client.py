import requests
from gevent import monkey
monkey.patch_all(ssl=False)  # ssl=false otherwise issue with requests
import websocket
import ssl
import json
import gevent
import pytz
from urllib.parse import urlencode
from datetime import datetime as dt
from arctic import Arctic, TICK_STORE


EST = pytz.timezone('US/Eastern')


def create_url(protocol, host, base_path, params):
    """Build request url"""
    params = ("?" + urlencode(params)) if params else ""
    url = f'{protocol}://{host}{base_path}'
    return url + params


class BinanceWebSocket:


    def __init__(self, api_key=None):
        self.api_key = api_key
        self.ws = None
        self.ssl_opt = {"cert_reqs": ssl.CERT_NONE}



class DepthSocket(BinanceWebSocket):
    # Should probably move these vals to a RESTConfig/WSConfig class
    rest_protocol = 'https'
    rest_host = 'www.binance.com'
    rest_base_path = '/api/v1/depth'
    ws_protocol = 'wss'
    ws_host = 'stream.binance.com'
    ws_port = '9443'
    ws_base_path = '/ws'

    def __init__(self, symbol, fetch_base=True, write=False, dbconn=None):
        super().__init__(api_key=None)
        self.symbol = symbol
        self.params = {'symbol': symbol}
        self.bids = {}
        self.asks = {}
        self.last_update_id = None
        self.timestamp = None
        self.write = write
        self.dbconn = dbconn
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
        if new_values['u'] > self.last_update_id:
            self.timestamp = new_values['E']
            self.last_update_id = new_values['u']
            new_bids = {k: v for k, v, _ in new_values['b']}
            new_asks = {k: v for k, v, _ in new_values['a']}
            for k, v in new_bids.items():
                self.bids[k] = v
                if v == '0.00000000':
                    del self.bids[k]
            for k, v in new_asks.items():
                self.asks[k] = v
                if v == '0.00000000':
                    del self.asks[k]

            # Dump to database
            if self.write:
                try:
                    self.dbconn.write(self.symbol, self.convert_to_arctic())
                except Exception as e:
                    print('Failed to write tick to database: \n %s' % e)
            else:
                print(self.symbol)
        else:
            print('Received stale data')
            pass

    def _on_message(self, ws, message):
        data = json.loads(message)
        self.update_book(data)

    def _on_error(self, ws, error):
        raise Exception(error)

    def stream(self):
        call_path = f'/{self.symbol.lower()}@depth'
        url = f'{self.ws_protocol}://{self.ws_host}:{self.ws_port}{self.ws_base_path}{call_path}'
        self.ws = websocket.WebSocketApp(url,
                                         on_message=self._on_message,
                                         on_error=self._on_error)
        self.ws.run_forever(sslopt=self.ssl_opt)

    def convert_to_arctic(self):
        db_input = {}
        db_input['index'] = dt.fromtimestamp(self.timestamp/1000.0, tz=EST)
        db_input['depth_id'] = self.last_update_id
        for n, bid in enumerate(self.bids.items()):
            db_input[f'bid{n}'] = bid[0]
            db_input[f'bid{n}_ammt'] = bid[1]
        for n, ask in enumerate(self.asks.items()):
            db_input[f'ask{n}'] = ask[0]
            db_input[f'ask{n}_ammt'] = ask[1]
        # print(db_input['bid1'] + ': ' + db_input['bid1_ammt'])
        return [db_input]


class OrderBook:
    """Collection of depth tickers?"""
    def __init__(self, symbols, data_lib=None, api_key=None):
        self.api_key = api_key
        self.symbols = symbols
        self.state = None
        self.dbconn = None
        self.initialize_db(data_lib)

    def initialize_db(self, lib):
        if lib:
            db = Arctic('localhost')
            if lib not in db.list_libraries():
                print('Data library \'%s\' does not exist -- creating it' % lib)
                db.initialize_library(lib, lib_type=TICK_STORE)
            self.dbconn = db[lib]


    def _on_update(self, values):
        """Specify what to do with new data"""
        print(values)
        gevent.sleep(0)

    def stream_orderbook(self, write=False):
        def hatch(sym):
            sock = DepthSocket(symbol=sym, dbconn=self.dbconn, write=write)
            sock.stream()
        bucket = self.symbols
        threads = [gevent.spawn(hatch, sym) for sym in bucket]
        gevent.joinall(threads)


if __name__ == '__main__':
    ticker = OrderBook(symbols=['BNBBTC', 'ETHBTC'], data_lib='binance.testbook')
    ticker.stream_orderbook(write=False)
