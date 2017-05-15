from tornado import gen
from tornado.ioloop import PeriodicCallback

from client.base import AbstractSender


class StatusSender(AbstractSender):
    """Объект отправки статуса устройства."""

    def __init__(self, client, request_cls, host, port, log):
        """Инициализация отправки статуса устройства.

        :param client: HTTP-клиент
        :type client: tornado.httpclient.AsyncHTTPClient

        :param request_cls: Класс объекта запроса
        :type request_cls: Type of emulate.client.request.StatusRequest

        :param host: Хост, на который отправится запрос
        :type host: str

        :param port: Порт, на который отправится запрос
        :type port: int

        :param log: Логгер
        :type log: logging.Logger
        """
        self.client = client
        self.request_cls = request_cls
        self.host = host
        self.port = port
        self.log = log

    @gen.coroutine
    def send(self):
        """Отправляет запрос."""
        request = self.get_request()
        self.log.info(
            'Send request (body = {}) to {}'.format(request.body, request.url))

        response = yield self.client.fetch(request)

        self.log.info(
            'Received response (body = {}) from {}'.format(
                response.body, response.effective_url))

    def get_url(self):
        """Возвращает url, на который отправится запрос."""
        return 'http://{host}:{port}/status/'.format(
            host=self.host, port=self.port)

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
