import json
import uuid

from tornado.httpclient import HTTPRequest


class StatusRequest(HTTPRequest):
    """Запрос статуса устройства."""

    def __init__(self, device_id, url):
        """Инициализация запроса отправки статуса устройства.

        :param ip_address: IP-адрес
        :type ip_address: str

        :param url: URL, на который отправить запрос
        :type url: str
        """
        body = json.dumps({
            'device_id': device_id,
            'request_id': str(uuid.uuid4()),
            'status': 'OK',
            'data': {}
        })
        super(StatusRequest, self).__init__(
            url=url,
            method='POST',
            headers={'Content-Type': 'application/json'},
            body=str(body)
        )
