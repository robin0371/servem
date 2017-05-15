"""Модуль запуска эмуляции устройств."""
import argparse

from client.emulator import DevicesEmulation


arg_parser = argparse.ArgumentParser(
    prog='servem', description='Конфигурация запуска эмулятора устройств')

arg_parser.add_argument(
    '--settings', type=open,  help='Путь к файлу настройки')
arg_parser.add_argument(
    '--devices_id', '-d', nargs='*', type=str, help='Идентификаторы устройств')
arg_parser.add_argument(
    '--host', '-ht', type=str, help='Хост, направления статуса')
arg_parser.add_argument(
    '--port', '-p', type=int,  help='Порт, направления статуса')


def start():
    """Запускает эмуляцию устройств."""
    args = arg_parser.parse_args()

    devices_emulation = DevicesEmulation(args.devices_id, args.host, args.port)
    devices_emulation.start()


if __name__ == '__main__':
    start()
