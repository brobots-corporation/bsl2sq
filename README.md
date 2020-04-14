# Поисковик bsl модулей для sonarqube

[![Build Status](https://travis-ci.org/brobots-corporation/bsl2sq.svg?branch=master)](https://travis-ci.org/brobots-corporation/bsl2sq)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=bsl2sq&metric=alert_status)](https://sonarcloud.io/dashboard?id=bsl2sq)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=bsl2sq&metric=coverage)](https://sonarcloud.io/dashboard?id=bsl2sq)
[![](https://img.shields.io/pypi/v/bsl2sq.svg?style=flat&color=blue)](https://pypi.org/project/bsl2sq/)
[![](https://img.shields.io/pypi/pyversions/bsl2sq.svg)](https://pypi.python.org/pypi/bsl2sq/)
[![](https://img.shields.io/badge/license-GPL3-yellow.svg)](https://github.com/brobots-corporation/bsl2sq/blob/master/LICENSE)

Поиск bsl файлов проекта (конфигурации 1С) по вхождению в подсистемы.

## Возможности

* Работа в ОС семейства: Linux, Windows, Mac OS X;
* Вывод полного или относительного пути к файлам с расширением .bsl;
* Вывод списка путей в файл sonar-project.properties или в поток стандартного вывода;
* Вывод кириллических символов в символах UNICODE.

## Установка и обновление

* Установить Python версии не ниже 3.6;
* Установить пакет bsl2sq из PyPI командой:
    ```sh
    pip install bsl2sq
    ```
* Для обновления пакета необходимо воспользоваться командой:
    ```sh
    pip install -U bsl2sq
    ```
> Анализ файлов выгрузки выполняется для платформы 1С версии не ниже 8.3.10.

## Использование модуля

`bsl2sq [-h] [-f FILE] [-a] [-u] [-v] [-V] sourcedirectory parseprefix` - структура вызова скрипта

Обязательные аргументы:
* `sourcedirectory` - путь к корневой папке с выгруженной конфигурацией 1с;
* `parseprefix` -  префиксы подсистем, в которых будет осуществляться поиск путей до файлов объектов метаданных. Разделителем префиксов является пробел, к примеру `рн_ пк_ зс_`
  
Опциональные параметры:
* `-h, --help` - вызов справки;
* `-f FILE, --file FILE` - полный путь к файлу sonar-project.properties, в который будет выполняться выгрузка путей объектов метаданных на место переменной `$inclusions_line`;
* `-a, --absolute` - в случае указания флага будут выгружаться полные пути к файлам. Без флага только относительные пути;
* `-u, --unicode` - в случае указания флага будут выгружаться все кириллические символы в символах unicode;
* `-v, --verbose` - в случае указания флага будут выводиться подробная информация;
* `-V, --version` - вывод версии скрипта.

Пример файла `sonar-project.properties` для первоначального запуска:

```properties
# Фильтры на включение в анализ. В примере ниже - только bsl и os файлы.
sonar.inclusions=$inclusions_line
```
При последующих запусках скрипт автоматически будет удалять предыдущий список  объектов и заполнять новыми в файле `sonar-project.properties`. Замена будет выполняться между двумя ключевыми словами `sonar.inclusions=` и `$inclusions_end`

### Пример использования скрипта в Linux

```sh
bsl2sq "/Users/gostmair/GitReps/rn_erp/src/conf" "рн_" -u -f "/Users/gostmair/GitReps/rn_erp/sonar-project.properties"
```

### Пример использования скрипта в Windows

```cmd
bsl2sq c:\PythonScripts\rn_erp\src\conf\ рн_ -u -f d:\rn_erp\sonar-project.properties
```