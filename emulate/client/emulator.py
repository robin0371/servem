import signal

from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado.log import enable_pretty_logging, app_log
from tornado.options import options

from emulate.base import StartInterface, StopInterface
from emulate.client.client import Device
from emulate.client.request import StatusRequest
from emulate.client.sender import PeriodicStatusSender


class DevicesEmulation(StartInterface, StopInterface):
    """Система эмуляции устройств."""

    def __init__(self, devices_ids, host, port):
        """Инициализация системы эмуляции устройств.

        :param devices_ids: ID устройств
        :type staging: list of str

        :param host: Хост сервера, на который устройства передают статус
        :type host: str

        :param port: Порт сервера, на который устройства передают статус
        :type port: int
        """
        self.devices_ids = devices_ids
        self.host = host
        self.port = port

    def start(self):
        """Запуск эмуляции устройств."""
        enable_pretty_logging(options)
        app_log.info('Starting the devices emulation system...')

        # Запускаем устройства(клиенты)
        for device_id in self.devices_ids:
            sender = PeriodicStatusSender(
                AsyncHTTPClient(), StatusRequest, self.host, self.port, app_log
            )
            device = Device(device_id, sender, app_log)
            device.start()

        self.io_loop = IOLoop.instance()

        # Сигнал на остановку эмуляции по нажатию Ctrl-C
        signal.signal(
            signal.SIGINT,
            lambda sig, frame: self.io_loop.add_callback_from_signal(self.stop)
        )

        self.io_loop.start()

    def stop(self):
        """Остановка эмуляции устройств."""
        self.io_loop.stop()
        app_log.info('The devices emulation system is stopped.')
