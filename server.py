"""Модуль запуска эмуляции серверов приложений."""
import argparse

from emulate import ServersEmulation


arg_parser = argparse.ArgumentParser(
    prog='servem', description='Конфигурация запуска эмуляции серверов')

arg_parser.add_argument(
    '--settings', type=open,  help='Путь к файлу настройки')
arg_parser.add_argument(
    '--staging_port', '-sp', type=int,  help='Порт сервера для разработки')
arg_parser.add_argument(
    '--production_like_port', '-plp', type=int,
    help='Порт сервера для регрессионного тестирования')
arg_parser.add_argument(
    '--production_port', '-pp', type=int,  help='Порт production-сервера')


def start():
    """Запускает серверы системы."""
    args = arg_parser.parse_args()

    servers_emulation = ServersEmulation(
        staging=args.staging_port,
        production_like=args.production_like_port,
        production=args.production_port
    )
    servers_emulation.start()


if __name__ == '__main__':
    start()
