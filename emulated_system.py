"""Модуль запуска эмуляции программно-аппаратной системы."""
import argparse

from simple_settings import settings
from tornado.httpclient import AsyncHTTPClient
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.log import enable_pretty_logging, app_log
from tornado.options import options
from tornado.web import Application

from emulate.actions import PeriodicStatusSender
from emulate.client import Device
from emulate.handlers import StatusHandler
from emulate.request import StatusRequest


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
    '--servers_ports', '-sp', nargs='*', type=int,  help='Порты серверов')


def start():
    """Запускает эмулятор программно-аппаратной системы."""
    args = arg_parser.parse_args()
    conf = settings.as_dict()

    enable_pretty_logging(options)
    app_log.info('Starting the emulation system...')

    application = Application([
        (r'/status/', StatusHandler)
    ])

    # Запускаем серверы
    for server_port in args.servers_ports:
        http_server = HTTPServer(application)
        http_server.listen(server_port)

    # Запускаем сервер по-умолчанию
    ds_conf = conf['DEFAULT_SERVER']
    default_server = HTTPServer(application)
    default_server.listen(ds_conf['PORT'], ds_conf['HOST'])

    # Запускаем устройства(клиенты)
    for device_id in args.devices_id:
        status_sender = PeriodicStatusSender(
            AsyncHTTPClient(), StatusRequest, args.host, args.port)
        device = Device(device_id, status_sender)
        device.start()

    IOLoop.instance().start()


if __name__ == '__main__':
    try:
        start()
    except KeyboardInterrupt:
        app_log.info('The emulation system is stopped.')
