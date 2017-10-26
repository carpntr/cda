import requests
from gevent import monkey
monkey.patch_all(ssl=False)  # ssl=false otherwise issue with requests
import websocket
import ssl
import json
import gevent
from urllib.parse import urlencode
from arctic import Arctic, TICK_STORE
from exchanges.binance.order_book import OrderBook



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
        self.order_book = OrderBook()
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
        self.order_book.initialize(depth_dict=depth)
        return resp.status_code

    def update_book(self, new_values):
        """Update state of the book"""
        self.order_book.update(new_values)
        # Dump to database
        if self.write:
            try:
                self.dbconn.write(self.symbol,
                                  self.order_book.dump(style='arctic'))
            except Exception as e:
                print('Failed to write tick to database: \n %s' % e)
        else:
            print(self.symbol)

    def _on_message(self, ws, message):
        data = json.loads(message)
        self.update_book(data)
        gevent.sleep(0)

    def _on_error(self, ws, error):
        raise Exception(error)

    def stream(self):
        call_path = f'/{self.symbol.lower()}@depth'
        url = f'{self.ws_protocol}://{self.ws_host}:{self.ws_port}{self.ws_base_path}{call_path}'
        self.ws = websocket.WebSocketApp(url,
                                         on_message=self._on_message,
                                         on_error=self._on_error)
        self.ws.run_forever(sslopt=self.ssl_opt)



class SocketManager:
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

    def stream_orderbook(self, write=False):
        def hatch(sym):
            sock = DepthSocket(symbol=sym, dbconn=self.dbconn, write=write)
            sock.stream()
        bucket = self.symbols
        threads = [gevent.spawn(hatch, sym) for sym in bucket]
        gevent.joinall(threads)



