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
