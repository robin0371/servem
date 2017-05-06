import json
import uuid

from tornado.httpclient import HTTPRequest


class StatusRequest(HTTPRequest):
    """Запрос статуса устройства."""

    def __init__(self, ip_address, port, device_id):
        """Инициализация запроса отправки статуса устройства.

        :param ip_address: IP-адрес
        :type ip_address: str

        :param port: Порт
        :type port: int

        :param device_id: ID устройства
        :type device_id: str
        """
        body = json.dumps({
            'device_id': device_id,
            'request_id': str(uuid.uuid4()),
            'status': 'OK',
            'data': {}
        })
        super(StatusRequest, self).__init__(
            url='http://{ip_address}:{port}/status/'.format(
                ip_address=ip_address, port=port),
            method='POST',
            headers={'Content-Type': 'application/json'},
            body=str(body)
        )
