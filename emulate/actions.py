from tornado.ioloop import PeriodicCallback
from tornado.log import app_log


class StatusSender(PeriodicCallback):
    """Объект отправки статуса устройства."""

    # Каждые 2 секунды
    callback_time = 2000

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
        super(StatusSender, self).__init__(self.send, self.callback_time)
        self.client = client
        self.request_cls = request_cls
        self.ip_address = ip_address
        self.port = port

    def send(self, request):
        """Отправляет запрос."""
        app_log.info('Send request (body = {})'.format(request.body))
        self.client.fetch(request)

    def get_request(self):
        """Возвращает запрос о состоянии."""
        return self.request_cls(self.ip_address, self.port, self.device_id)

    def _run(self):
        if not self._running:
            return
        try:
            request = self.get_request()
            return self.callback(request)
        except Exception:
            self.io_loop.handle_callback_exception(self.callback)
        finally:
            self._schedule_next()
