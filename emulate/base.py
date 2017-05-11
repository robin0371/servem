from abc import ABCMeta, abstractmethod


class StartInterface(object):
    """Интерфейс старта."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self):
        """Запуск."""


class StopInterface(object):
    """Интерфейс остановки."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def stop(self):
        """Остановка."""


class AbstractDevice(StartInterface, StopInterface):
    """Абстрактный объект устройства."""

    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def device_id(self):
        """ID устройства."""

    @device_id.setter
    @abstractmethod
    def device_id(self, value):
        """Установка значения ID устройства."""


class AbstractSender(StartInterface, StopInterface):
    """Абстрактный объект отправителя."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def send(self):
        """Отправка."""

    @abstractmethod
    def get_request(self):
        """Возвращает объект, отправляющегося запроса."""

    @property
    @abstractmethod
    def get_url(self):
        """Возвращает URL, на который происходит отправление."""


class AbstractAppInstance(StartInterface, StopInterface):
    """Абстрактный инстанс приложения."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def set_app(self):
        """Инициализирует приложение."""

    @abstractmethod
    def set_server(self):
        """Инициализирует сервер."""


class AbstractDeviceFactory(object):
    """Абстрактная фабрика инстансов устройств."""

    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def client_cls(self):
        """Клиент отправки статуса."""

    @property
    @abstractmethod
    def sender_cls(self):
        """Отправитель статуса."""

    @property
    @abstractmethod
    def request_cls(self):
        """Запрос статуса."""

    @abstractmethod
    def create(self):
        """Создает устройство."""
