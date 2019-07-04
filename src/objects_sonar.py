import sys
import argparse
import os
import glob
import xml.dom.minidom as minidom
import re

# Создание парсера аргументов командной строки
def createparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('sourcedirectory', type=str,
                        help='путь к корневой папке с выгруженной конфигурацией 1с')
    parser.add_argument('parseprefix', type=str,
                        help='префикс подсистем, в которых будет осуществляться поиск путей до файлов объектов метаданных')
    parser.add_argument('-f', '--file', type=str, default="",
                        help='полный путь к файлу, в который будет выполняться выгрузка путей объектов метаданных')
    parser.add_argument('-a', '--absolute', action='store_const', const=True, default=False,
                        help='в случае указания флага будут выгружаться полные пути к файлам. без флага только относительные пути')

    return parser

# Процедура проверки аргументов командной строки
def checkargs(args):
    # Проверка существования указанной папки
    if not os.path.exists(args.sourcedirectory):
        print(args.sourcedirectory+" - папка не существует")
        sys.exit()
    # Проверка, что по указанному пути находится папка
    if not os.path.isdir(args.sourcedirectory):
        print(args.sourcedirectory+" - это не папка")
        sys.exit()
    # Проверка указания не пустого префикса для подсистем
    if len(args.parseprefix) == 0:
        print("необходимо указать не пустой префикс")
        sys.exit()

# Парсинг xml файлов подсистем, для получения списка объектов
def getObjects(file):
    # Парсинг файла до тегов item
    doc = minidom.parse(file)
    sub_items = doc.getElementsByTagName("MetaDataObject")[0].getElementsByTagName("Subsystem")[0].getElementsByTagName("Properties")[0].getElementsByTagName("Content")[0].getElementsByTagName("xr:Item")
    
    # Маска поиска guid удаленных объектов, которые остались в подсистемах, чтобы их исключить
    mask = "[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
    metadata = set()
    for item in sub_items:
        obj = item.childNodes[0].data
        # Проверка результата, что он является путем к объекту, а не guid
        if not re.match(mask, obj):
            metadata.add(item.childNodes[0].data)
    
    return metadata

# Получение парсера и разбор параметров командной строки
parser = createparser()
args = parser.parse_args()

# Проверка аргументов командной строки
checkargs(args)

SUBSYSTEMS_PATH = ""

# проверка окончания пути
if args.sourcedirectory[-1] == "/":
    SUBSYSTEMS_PATH = args.sourcedirectory+"subsystems/"
else:
    SUBSYSTEMS_PATH = args.sourcedirectory+"/subsystems/"

# установка текущий директории
os.chdir(SUBSYSTEMS_PATH)
# поиск файлов подсистем с заданным префиксом
subsystems_files = glob.glob("**/"+args.parseprefix+"*.xml", recursive=True)

set_metadata = set()
list_metadata = []

for file in subsystems_files:
    # with open(SUBSYSTEMS_PATH+file) as xml_file:
    #     xml_body = xml_file.read()
    for obj in getObjects(SUBSYSTEMS_PATH+file):
        set_metadata.add(obj)

list_metadata = list(set_metadata)
list_metadata.sort()

linenum = 1
for li in list_metadata:
    print(str(linenum)+". "+li)
    linenum = linenum + 1