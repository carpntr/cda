import requests
import json
import pprint
import asyncio
import websocket


class CCWebSocket:
    ws_protocol = 'wss'
    ws_host = 'streamer.cryptocompare.com'

    def __init__(self):
        self.url = f'{self.ws_protocol}://{self.ws_host}'
        self.ws = websockets
    def add_sub(self):
        sub_string = {'subs':['0~Poloniex~BTC~USD']}
        self.ws.send(json.dumps(sub_string))
        self.ws.run_forever()

    def stream(self):
        self.ws = websocket.WebSocketApp(self.url,
                                         on_message=self._handle_message,
                                         on_error=self._handle_message)


    def _handle_message(self, ws, msg):
        print(msg)

sock = CCWebSocket()
sock.add_sub()
