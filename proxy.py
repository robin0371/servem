"""Модуль запуска proxy-сервера маршрутизации."""
import argparse

from server.proxy.server import ProxyServer


arg_parser = argparse.ArgumentParser(
    prog='proxy', description='Конфигурация запуска proxy-сервера')

arg_parser.add_argument(
    '--settings', type=open,  help='Настройки proxy-сервера')
arg_parser.add_argument(
    '--host', '-ht', type=str, help='Хост, proxy-сервера')
arg_parser.add_argument(
    '--port', '-p', type=int,  help='Порт, proxy-сервера')


def start():
    """Запускает proxy-сервер маршрутизации."""
    args = arg_parser.parse_args()

    proxy_instance = ProxyServer(args.host, args.port)
    proxy_instance.start()


if __name__ == '__main__':
    start()
