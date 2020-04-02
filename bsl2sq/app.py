from .cliparser import CliParser
from .bslfinder import BslFinder


def bsl2sq() -> None:
    """ Поиск и вывод данных для анализа в sonarqube
    """

    cli_args = CliParser().args
    BslFinder(cli_args).data_to_sq()


if __name__ == "__main__":
    bsl2sq()
