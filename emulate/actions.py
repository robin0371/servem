from tornado.ioloop import PeriodicCallback
from tornado.log import app_log

from emulate.base import AbstractSender


class StatusSender(AbstractSender):
    """Объект отправки статуса устройства."""

    def __init__(self, client, request_cls, ip_address, port):
        """Инициализация отправки статуса устройства.

        :param client: HTTP-клиент
        :type client: tornado.httpclient.AsyncHTTPClient

        :param request_cls: Класс объекта запроса
        :type request_cls: Type of emulate.request.StatusRequest

        :param ip_address: IP-адрес
        :type ip_address: str

        :param port: Порт
        :type port: int
        """
        self.client = client
        self.request_cls = request_cls
        self.ip_address = ip_address
        self.port = port

    def send(self):
        """Отправляет запрос."""
        request = self.get_request()
        app_log.info('Send request (body = {})'.format(request.body))
        self.client.fetch(request)

    def get_url(self):
        """Возвращает url, на который отправится запрос."""
        return 'http://{ip_address}:{port}/status/'.format(
            ip_address=self.ip_address, port=self.port)

    def get_request(self):
        """Возвращает объект запроса."""
        return self.request_cls(self.device_id, self.get_url())

    def start(self):
        """Начинает отправку статуса."""
        self.send()

    def stop(self):
        """Завершение отправки статуса."""
        pass


class PeriodicStatusSender(StatusSender):
    """Объект периодической отправки статуса устройства."""

    # Каждые 2 секунды
    callback_time = 2000

    def start(self):
        """Начинает отправку статуса."""
        self.periodic_sender = PeriodicCallback(self.send, self.callback_time)
        self.periodic_sender.start()

    def stop(self):
        """Завершение отправки статуса."""
        self.periodic_sender.stop()
