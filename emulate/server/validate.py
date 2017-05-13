from cerberus import Validator


# Схема валидации тела запроса
STATUS_SCHEMA = {
    'device_id': {'type': 'string', 'required': True},
    'request_id': {'type': 'string', 'min': 16, 'max': 16, 'required': True},
    'status': {'type': 'string', 'required': True},
    'data': {'type': 'dict', 'required': True},
}


def validate_status_request(body):
    """Валидирует тело запроса статуса устройства.

    :param body: Словарь тела запроса
    :type body: dict

    :return Результат валидации и причина, если значение не валидно
    :rtype tuple(bool, str)
    """
    reason = ''
    is_validate = Validator().validate(body, STATUS_SCHEMA)

    if not is_validate:
        reason = ('Request body ({}) is not validated to schema ({}).'
                  ''.format(body, STATUS_SCHEMA))

    return is_validate, reason
