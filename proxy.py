"""Модуль запуска proxy-сервера маршрутизации запросов системы."""
import argparse

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.log import app_log, enable_pretty_logging
from tornado.options import options
from tornado.web import Application

from emulate.handlers import ProxyStatusHandler


arg_parser = argparse.ArgumentParser(
    prog='proxy', description='Конфигурация запуска proxy-сервера')

arg_parser.add_argument(
    '--settings', '-s', type=open,  help='Маппинг серверов')
arg_parser.add_argument(
    '--host', '-ht', type=str, help='Хост, proxy-сервера')
arg_parser.add_argument(
    '--port', '-p', type=int,  help='Порт, proxy-сервера')


def start():
    """Запускает proxy-сервер для маршрутизации запросов."""
    args = arg_parser.parse_args()

    enable_pretty_logging(options)
    app_log.info('Starting proxy...')

    application = Application([
        (r'/status/', ProxyStatusHandler)
    ])

    proxy_server = HTTPServer(application, xheaders=True)
    proxy_server.listen(args.port, args.host)

    IOLoop.instance().start()


if __name__ == '__main__':
    try:
        start()
    except KeyboardInterrupt:
        app_log.info('Proxy is stopped.')
