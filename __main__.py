import argparse

from simple_settings import settings
from tornado.httpclient import AsyncHTTPClient
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.log import enable_pretty_logging, app_log
from tornado.options import options
from tornado.web import Application

from emulate.actions import StatusSender
from emulate.client import Device
from emulate.request import StatusRequest
from handlers import StatusHandler
from proxy import HTTPProxyServer


arg_parser = argparse.ArgumentParser(
    prog='servem',
    description='Конфигурация запуска эмулятора программно-аппаратной системы')

arg_parser.add_argument(
    '--settings', '-s', type=open,  help='Маппинг серверов')
arg_parser.add_argument(
    '--device_id', '-d', nargs='*', type=str, help='Идентификаторы устройств')
arg_parser.add_argument(
    '--ip', '-i', nargs='*', type=str, help='IP-адреса устройств')
arg_parser.add_argument(
    '--port', '-p', nargs='*', type=int,  help='Порты устройств')
arg_parser.add_argument(
    '--server_port', '-sp', nargs='*', type=int,  help='Порты серверов')


def start():
    """Запускает эмулятор программно-аппаратной системы."""
    args = arg_parser.parse_args()
    server_map = settings.as_dict()

    enable_pretty_logging(options)
    app_log.info('Starting the emulation system...')

    application = Application([
        (r'/status/', StatusHandler)
    ])

    # proxy_server = HTTPProxyServer(application)

    # Запускаем серверы
    for server_port in args.server_port:
        http_server = HTTPServer(application)
        http_server.listen(server_port)

    # Запускаем устройства(клиенты)
    for index, device_id in enumerate(args.device_id):
        # status_request = StatusRequest(
        #     args.ip[index], args.port[index],
        #     # server_map['DEFAULT']['SERVER'],
        #     # server_map['DEFAULT']['PORT'],
        #     device_id,
        # )
        status_sender = StatusSender(
            AsyncHTTPClient(), StatusRequest, args.ip[index], args.port[index])
        device = Device(device_id, status_sender)
        device.start()

    IOLoop.instance().start()


if __name__ == '__main__':
    try:
        start()
    except KeyboardInterrupt:
        app_log.info('The emulation system is stopped.')
