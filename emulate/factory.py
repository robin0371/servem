from tornado.httpclient import AsyncHTTPClient
from tornado.httpserver import HTTPServer
from tornado.web import Application

from emulate.actions import StatusSender, PeriodicStatusSender
from emulate.base import AbstractAppInstanceFactory, AbstractDeviceFactory
from emulate.client import Device
from emulate.handlers import StatusHandler, ProxyStatusHandler
from emulate.request import StatusRequest


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
        """Инициализирует приложение."""
        self.app = Application([
            (r'/status/', StatusHandler)
        ])

    def set_server(self):
        """Инициализирует сервер."""
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


class ProxyInstance(AppInstanceFactory):
    """Инстанс приложения для проксирования."""

    name = 'proxy'

    def set_app(self):
        """Инициализирует приложение."""
        self.app = Application([
            (r'/status/', ProxyStatusHandler)
        ])

    def set_server(self):
        """Инициализирует сервер."""
        self.server = HTTPServer(self.app, xheaders=True)


class DeviceFactory(AbstractDeviceFactory):
    """Фабрика устройств, отправляющих свой статус.

    Базовый класс для инициализации устройства.
    """

    client_cls = AsyncHTTPClient
    sender_cls = StatusSender
    request_cls = StatusRequest

    def __init__(self, device_id, host=None, port=None):
        """Инициализация инстанса приложения.

        :param device_id: ID устройства
        :type device_id: str

        :param host: Хост
        :type host: str

        :param port: Порт
        :type port: int
        """
        self.device_id = device_id
        self.host = host
        self.port = port

    def create(self):
        """Создает и возвращает устройство."""
        client = self.client_cls()
        sender = self.sender_cls(
            client, self.request_cls, self.host, self.port)
        device = Device(self.device_id, sender)

        return device


class TerminalFactory(DeviceFactory):
    """Фабрика терминалов, периодически отправляющих свой статус."""

    sender_cls = PeriodicStatusSender
