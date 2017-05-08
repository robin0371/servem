

class RedirectMapper(object):
    """Маппер перенаправлений запросов."""

    def __init__(self, schema):
        """Инициализация маппинга перенаправлений запросов.

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
        for host, port_map in self.schema.items():
            for port, terminals_list in port_map.items():
                if device_id in terminals_list:
                    return host, port

        return default
