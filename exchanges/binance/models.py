import simplejson
import ssl
import websocket

from events import Events


class WebSocket(Events):
    __events__ = ['callback']

    def __init__(self, api, callback=None):
        self.api = api
        self.callback += callback

    def _full_url(self, path):
        return "%s://%s:%s%s%s" % (self.api.protocol,
                                self.api.host,
                                self.api.port,
                                self.api.base_path,
                                path)

    def _on_message(self, ws, message):
        data = simplejson.loads(message)
        self.callback(data)

    def _on_error(self, ws, error):
        raise Exception(error)

    def prepare_request(self, path):
        url = self._full_url(path)

        return url

    def run_forever(self, url):
        self.ws = websocket.WebSocketApp(url,
                                         on_message=self._on_message,
                                         on_error=self._on_error)
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})