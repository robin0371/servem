from cerberus import Validator
from tornado import web


# Схема валидации тела запроса
STATUS_SCHEMA = {
    'device_id': {'type': 'string'},
    'request_id': {'type': 'string', 'min': 16, 'max': 16},
    'status': {'type': 'string'},
    'data': {'type': 'dict'},
}


def validate_status_request(body):
    """Валидирует тело запроса статуса устройства.

    :param body: Словарь тела запроса
    :type body: dict

    :raise tornado.web.HTTPError
    """
    is_validate = Validator().validate(body, STATUS_SCHEMA)

    if not is_validate:
        raise web.HTTPError(
            400, 'Request body ({}) is not validated to schema ({}).'
                 ''.format(body, STATUS_SCHEMA))
