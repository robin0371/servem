from client.base import AbstractDevice


class Device(AbstractDevice):
    """Устройство."""

    def __init__(self, device_id, status_sender, log):
        """Инициализация устройства.

        :param device_id: ID устройства
        :type device_id: str

        :param status_sender: Отправитель статуса
        :type status_sender: emulate.client.sender.StatusSender

        :param log: Логгер
        :type log: logging.Logger
        """
        self.device_id = device_id
        self.status_sender = status_sender
        self.status_sender.device_id = device_id
        self.log = log

    @property
    def device_id(self):
        return self._device_id

    @device_id.setter
    def device_id(self, value):
        self._device_id = value

    def start(self):
        """Включает устройство."""
        self.log.info('Start device ID = {}'.format(self.device_id))
        self.status_sender.start()

    def stop(self):
        """Выключает устройство."""
        self.log.info('Stopped device ID = {}'.format(self.device_id))
        self.status_sender.stop()
