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
        """Отправляющийся запрос."""

    @property
    @abstractmethod
    def get_url(self):
        """URL, на который происходит отправление."""
