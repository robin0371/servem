from tornado.httpserver import HTTPServer
from tornado.web import Application

from emulate.base import AbstractAppInstanceFactory
from emulate.handlers import StatusHandler


class AppInstanceFactory(AbstractAppInstanceFactory):
    """Фабрика инстансов приложений.

    Базовый класс для инициализации приложения принимающего статус устройств.
    """

    def __init__(self, host=None, port=None):
        """Инициализация инстанса приложения.

        :param host: Хост
        :type host: str

        :param port: Порт
        :type port: int
        """
        self.host = host
        self.port = port

    def set_app(self):
        """Инициализирует."""
        self.app = Application([
            (r'/status/', StatusHandler)
        ])

    def set_server(self):
        self.server = HTTPServer(self.app)

    def start(self):
        self.set_app()
        self.set_server()
        self.server.listen(self.port, self.host)


class StagingInstance(AppInstanceFactory):
    """Инстанс приложения для разработки."""

    name = 'staging'


class ProductionLikeInstance(AppInstanceFactory):
    """Инстанс приложения для регрессионного тестирования."""

    name = 'production-like'


class ProductionInstance(AppInstanceFactory):
    """Инстанс приложения для продакшена."""

    name = 'production'


class DefaultInstance(AppInstanceFactory):
    """Инстанс приложения для перенаправления по-умолчанию."""

    name = 'default'
