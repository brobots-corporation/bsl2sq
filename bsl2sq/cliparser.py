import argparse
import os
from .__version__ import __version__
import logging


class CliParser:

    def __init__(self) -> None:
        super().__init__()
        self.__version = __version__
        self.parser = self.create_parser()

    def create_parser(self) -> argparse.ArgumentParser:

        # Создание парсера аргументов командной строки
        parser = argparse.ArgumentParser()
        parser.add_argument('sourcedirectory', type=str,
                            help='путь к корневой папке с выгруженной конфигурацией 1с')
        parser.add_argument('parseprefix', type=str,
                            help='префикс подсистем, в которых будет осуществляться поиск путей до \
                                файлов объектов метаданных')
        parser.add_argument('-f', '--file', type=str, default="",
                            help='полный путь к файлу sonar-project.properties, в который будет выполняться \
                                выгрузка путей объектов метаданных на место переменной $inclusions_line')
        parser.add_argument('-a', '--absolute', action='store_const', const=True, default=False,
                            help='в случае указания флага будут выгружаться полные пути к файлам. без флага \
                                только относительные пути')
        parser.add_argument('-u', '--unicode', action='store_const', const=True, default=False,
                            help='в случае указания флага будут выгружаться все кириллические символы в \
                                символах unicode')
        parser.add_argument('-v', '--verbose', action='store_const', const=True, default=False,
                            help='выводить описание выполняемых операций')
        parser.add_argument('-V', '--version', action='version', version=self.__version,
                            help='вывести номер версии')

        return parser

    def check_args(self, args) -> None:

        # Процедура проверки аргументов командной строки
        # Проверка существования указанной папки

        if not os.path.exists(args.sourcedirectory):
            print(args.sourcedirectory + " - папка не существует")
            quit
        # Проверка, что по указанному пути находится папка
        if not os.path.isdir(args.sourcedirectory):
            print(args.sourcedirectory + " - это не папка")
            quit
        # Проверка указания не пустого префикса для подсистем
        if len(args.parseprefix) == 0:
            print("необходимо указать не пустой префикс")
            quit
        # Проверка, что по указанному пути находится папка
        if len(args.file) != 0 and not os.path.exists(args.file):
            print("файл sonar-project.properties по указанному пути не найден")
            quit

        # Вывод подробного лога выполнения
        if args.verbose:
            logging.info(f">>> Абсолютный путь к исходным файлам проекта: {os.path.abspath(args.sourcedirectory)}")
            logging.info(f">>> Абсолютный путь к исходным файлу sonar-project.properties: {os.path.abspath(args.file)}")

    @property
    def args(self) -> argparse.ArgumentParser:
        args = self.parser.parse_args()
        self.check_args(args)
        return vars(args)
