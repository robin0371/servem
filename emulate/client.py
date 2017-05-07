from tornado.log import app_log

from emulate.base import AbstractDevice


class Device(AbstractDevice):
    """Устройство."""

    def __init__(self, device_id, status_sender):
        """Инициализация устройства.

        :param device_id: ID устройства
        :type device_id: str

        :param status_sender: Отправитель статуса
        :type status_sender: emulate.actions.StatusSender
        """
        self.device_id = device_id
        self.status_sender = status_sender

    @property
    def device_id(self):
        return self._device_id

    @device_id.setter
    def device_id(self, value):
        self._device_id = value

    def start(self):
        """Включает устройство."""
        app_log.info('Start device ID = {}'.format(self.device_id))
        self.status_sender.start()

    def stop(self):
        """Выключает устройство."""
        app_log.info('Stopped device ID = {}'.format(self.device_id))
        self.status_sender.stop()
