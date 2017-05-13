from abc import ABCMeta, abstractmethod


class StartInterface(object):
    """Интерфейс запуска."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self):
        """Запуск."""


class StopInterface(object):
    """Интерфейс завершения."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def stop(self):
        """Завершение."""
