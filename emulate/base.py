from abc import ABCMeta, abstractmethod


class StartStopInterface(object):
    """Интерфейс старта и остановки."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self):
        """Запуск."""

    @abstractmethod
    def stop(self):
        """Остановка."""


class AbstractDevice(StartStopInterface):
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
