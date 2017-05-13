import signal

from simple_settings import settings
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.log import app_log, enable_pretty_logging
from tornado.options import options
from tornado.web import Application

from emulate.server.handlers import StatusHandler


class AppServer(object):
    """Сервер приложения."""

    def __init__(self, host=None, port=None):
        """Инициализация сервера приложения.

        :param host: Хост
        :type host: str

        :param port: Порт
        :type port: int
        """
        self.host = host
        self.port = port

    def set_app(self):
        """Инициализирует приложение."""
        self.app = Application([
            (r'/status/', StatusHandler)
        ])

    def set_server(self):
        """Инициализирует сервер."""
        self.server = HTTPServer(self.app)

    def start(self):
        """Запуск сервера приложения."""
        self.set_app()
        self.set_server()
        self.server.listen(self.port, self.host)


class ServersEmulation(object):
    """Система эмуляции серверов приложений."""

    def __init__(self, staging, production_like, production):
        """Инициализация системы эмуляции серверов приложений.

        :param staging: Порт staging-сервера
        :type staging: int

        :param production_like: Порт production-like-сервера
        :type production_like: int

        :param production: Порт production-сервера
        :type production: int
        """
        self.staging_port = staging
        self.production_like_port = production_like
        self.production_port = production
        self.io_loop = IOLoop.instance()

    def start(self):
        """Запуск серверов приложений."""
        conf = settings.as_dict()

        enable_pretty_logging(options)
        app_log.info('Starting the servers emulation...')

        # Запускаем серверы
        staging = AppServer(port=self.staging_port)
        staging.start()

        production_like = AppServer(port=self.production_like_port)
        production_like.start()

        production = AppServer(port=self.production_port)
        production.start()

        host, port = conf['DEFAULT_SERVER'].split(':')
        default = AppServer(host=host, port=port)
        default.start()

        # Сигнал на остановку эмуляции по нажатию Ctrl-C
        signal.signal(
            signal.SIGINT,
            lambda sig, frame: self.io_loop.add_callback_from_signal(self.stop)
        )

        self.io_loop.start()

    def stop(self):
        """Остановка серверов приложений."""
        self.io_loop.stop()
        app_log.info('The servers emulation is stopped.')
