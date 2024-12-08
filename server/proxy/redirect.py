

class RedirectResolver(object):
    """Объект для определения перенаправлений запросов."""

    def __init__(self, schema):
        """Инициализация объекта перенаправлений запросов.

        :param schema: Словарь - таблица перенаправлений
        :type schema: dict
        """
        self.schema = schema

    def get_redirect_address(self, device_id, default):
        """Возвращает кортеж (host, port), перенаправления для устройства.

        :param device_id: ID устройства
        :type device_id: str

        :param default: Кортеж (host, port) по-умолчанию
        :type default: tuple

        :rtype tuple
        """
        device_number = device_id.split('_')[1]

        for mapping in self.schema:
            host = mapping['host']
            port = mapping['port']
            begin, end = mapping['devices'].split('-')

            if int(device_number) in range(int(begin), int(end)):
                return host, port

        return default

