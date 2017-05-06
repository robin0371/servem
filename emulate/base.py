from abc import ABCMeta, abstractmethod


class AbstractDevice(object):
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

    @abstractmethod
    def start(self):
        """Включает устройство."""

    @abstractmethod
    def stop(self):
        """Останавливает устройство."""
