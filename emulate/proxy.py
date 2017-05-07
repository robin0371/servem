from tornado.httpserver import HTTPServer


class HTTPProxyServer(HTTPServer):
    """Proxy-сервер, для маршрутизации запросов устройств.
    
    Маршрутизирует запросы по маппингу из servermap.yaml.
    """

    def start_request(self, server_conn, request_conn):
        a = 2
