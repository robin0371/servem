from tornado.ioloop import PeriodicCallback
from tornado.log import app_log


class StatusSender(PeriodicCallback):
    """Объект отправки статуса устройства."""

    # Каждые 2 секунды
    callback_time = 2000

    def __init__(self, client, request):
        """Инициализация отправки статуса устройства.

        :param client: HTTP-клиент
        :type client: tornado.httpclient.AsyncHTTPClient

        :param request: Запрос
        :type request: emulate.request.StatusRequest
        """
        super(StatusSender, self).__init__(self.send, self.callback_time)
        self.client = client
        self.request = request

    def send(self):
        """Отправляет запрос."""
        app_log.info('Send request (body = {})'.format(self.request.body))
        self.client.fetch(self.request)
