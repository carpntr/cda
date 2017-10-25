from exchanges.binance.client import BinanceRESTAPI, BinanceWebSocketAPI

class SocketFeed:
    def __init__(self, datastream):
        self.stream = datastream

    def listen(self):
        pass