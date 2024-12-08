from cerberus import Validator


# Схема валидации тела запроса
STATUS_SCHEMA = {
    'device_id': {
        'type': 'string', 'regex': "^[a-z]{1,10}[_]{1}[0-9]+$", 'required': True},
    'request_id': {'type': 'string', 'min': 16, 'max': 16, 'required': True},
    'status': {'type': 'string', 'required': True},
    'data': {'type': 'dict', 'required': True},
}


def validate_status_request(body):
    """Валидирует тело запроса статуса устройства.

    :param body: Словарь тела запроса
    :type body: dict

    :return Результат валидации и словарь ошибок, если значение не валидно
    :rtype tuple(bool, dict)
    """
    validator = Validator()
    is_validate = validator.validate(body, STATUS_SCHEMA)

    return is_validate, validator.errors
