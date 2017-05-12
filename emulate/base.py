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
