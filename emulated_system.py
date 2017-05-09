"""Модуль запуска эмуляции программно-аппаратной системы."""
import argparse

from simple_settings import settings
from tornado.ioloop import IOLoop
from tornado.log import enable_pretty_logging, app_log
from tornado.options import options

from emulate.factory import (
    DefaultInstance,
    ProductionLikeInstance,
    ProductionInstance,
    StagingInstance,
    TerminalFactory
)


arg_parser = argparse.ArgumentParser(
    prog='servem',
    description='Конфигурация запуска эмулятора программно-аппаратной системы')

arg_parser.add_argument(
    '--settings', '-s', type=open,  help='Путь к файлу настройки')
arg_parser.add_argument(
    '--devices_id', '-d', nargs='*', type=str, help='Идентификаторы устройств')
arg_parser.add_argument(
    '--host', '-ht', type=str, help='Хост, направления статуса')
arg_parser.add_argument(
    '--port', '-p', type=int,  help='Порт, направления статуса')
arg_parser.add_argument(
    '--staging_port', '-sp', type=int,  help='Порт сервера для разработки')
arg_parser.add_argument(
    '--production_like_port', '-plp', type=int,
    help='Порт сервера для регрессионного тестирования')
arg_parser.add_argument(
    '--production_port', '-pp', type=int,  help='Порт продакшен-сервера')


def start():
    """Запускает эмулятор программно-аппаратной системы."""
    args = arg_parser.parse_args()
    conf = settings.as_dict()

    enable_pretty_logging(options)
    app_log.info('Starting the emulation system...')

    # Запускаем серверы
    staging = StagingInstance(port=args.staging_port)
    staging.start()

    production_like = ProductionLikeInstance(port=args.production_like_port)
    production_like.start()

    production = ProductionInstance(port=args.production_port)
    production.start()

    host, port = conf['DEFAULT_SERVER'].split(':')
    default = DefaultInstance(host=host, port=port)
    default.start()

    # Запускаем устройства(клиенты)
    for device_id in args.devices_id:
        device = TerminalFactory(device_id, args.host, args.port).create()
        device.start()

    IOLoop.instance().start()


if __name__ == '__main__':
    try:
        start()
    except KeyboardInterrupt:
        app_log.info('The emulation system is stopped.')
