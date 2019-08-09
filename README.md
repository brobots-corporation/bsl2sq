# BSL objects finder

[![Build Status](https://travis-ci.org/brobots-team/bsl-objects-to-analyze-sonar.svg?branch=master)](https://travis-ci.org/brobots-team/bsl-objects-to-analyze-sonar) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=bsl-objects-to-analyze-sonar&metric=alert_status)](https://sonarcloud.io/dashboard?id=bsl-objects-to-analyze-sonar)

Поиск bsl файлов проекта (конфигурации 1С) по вхождению в подсистемы

## Возможности

* Работа в ОС семейства: Linux, Windows, Mac OS X;
* Вывод полного или относительного пути к файлам с расширением .bsl;
* Вывод списка путей в файл sonar-project.properties или в поток стандартного вывода;
* Вывод кириллических символов в символах UNICODE.

## Установка и обновление

* Установить Python версии не ниже 3.5;
* Анализ файлов выгрузки выполняется для платформы 1С версии не ниже 8.3.10;
* Разместить файл objects_sonar.py в месте использования.


## Использование скрипта

`objects_sonar.py [-h] [-f FILE] [-a] [-u] sourcedirectory parseprefix` - структура вызова скрипта

Обязательные аргументы:
* `sourcedirectory` - путь к корневой папке с выгруженной конфигурацией 1с;
* `parseprefix` -  префикс подсистем, в которых будет осуществляться поиск путей до файлов объектов метаданных.
  
Опциональные параметры:
* `-h, --help` - вызов справки;
* `-f FILE, --file FILE` - полный путь к файлу sonar-project.properties, вкоторый будет выполняться выгрузка путей объектов метаданных на место переменной `$inclusions_line`;
* `-a, --absolute` - в случае указания флага будут выгружаться полные пути к файлам. Без флага только относительные пути;
* `-u, --unicode` - в случае указания флага будут выгружаться все кириллические символы в символах unicode.

Пример файла `sonar-project.properties` для первоначального запуска:

```properties
# Фильтры на включение в анализ. В примере ниже - только bsl и os файлы.
sonar.inclusions=$inclusions_line
```
При последующих запусках скрипт автоматические будет удалять список старых объектов и заполнять новым в файле `sonar-project.properties`

### Пример использования скрипта в Linux

```sh
python objects_sonar.py "/Users/gostmair/GitReps/rn_erp/src/conf" "рн_" -u -f "/Users/gostmair/GitReps/rn_erp/sonar-project.properties"
```

### Пример использования скрипта в Windows

```sh
python c:\PythonScripts\objects_sonar.py c:\PythonScripts\rn_erp\src\conf\ рн_ -u -f d:\rn_erp\sonar-project.properties
```