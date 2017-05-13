import signal

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.log import enable_pretty_logging, app_log
from tornado.options import options
from tornado.web import Application

from proxy.handlers import ProxyStatusHandler


class ProxyServer(object):
    """Proxy-сервер."""

    def __init__(self, host=None, port=None):
        """Инициализация proxy-сервера.

        :param host: Хост
        :type host: str

        :param port: Порт
        :type port: int
        """
        self.host = host
        self.port = port
        self.io_loop = IOLoop.instance()

    def set_app(self):
        """Инициализирует приложение."""
        self.app = Application([
            (r'/status/', ProxyStatusHandler)
        ])

    def set_server(self):
        """Инициализирует proxy-сервер."""
        self.server = HTTPServer(self.app, xheaders=True)

    def start(self):
        """Запуск proxy-сервера."""
        enable_pretty_logging(options)
        app_log.info('Starting proxy-server...')

        self.set_app()
        self.set_server()
        self.server.listen(self.port, self.host)

        # Сигнал на остановку эмуляции по нажатию Ctrl-C
        signal.signal(
            signal.SIGINT,
            lambda sig, frame: self.io_loop.add_callback_from_signal(self.stop)
        )

        self.io_loop.start()

    def stop(self):
        """Остановка proxy-сервера."""
        self.io_loop.stop()
        app_log.info('Proxy-server is stopped.')
