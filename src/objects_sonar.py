import sys
import argparse
import os
import glob
import xml.dom.minidom as minidom
import re

# Создание парсера аргументов командной строки
def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('sourcedirectory', type=str,
                        help='путь к корневой папке с выгруженной конфигурацией 1с')
    parser.add_argument('parseprefix', type=str,
                        help='префикс подсистем, в которых будет осуществляться поиск путей до файлов объектов метаданных')
    parser.add_argument('-f', '--file', type=str, default="",
                        help='полный путь к файлу, в который будет выполняться выгрузка путей объектов метаданных')
    parser.add_argument('-a', '--absolute', action='store_const', const=True, default=False,
                        help='в случае указания флага будут выгружаться полные пути к файлам. без флага только относительные пути')
    parser.add_argument('-u', '--unicode', action='store_const', const=True, default=False,
                        help='в случае указания флага будут выгружаться значение в виде символов Unicode')

    return parser

# Процедура проверки аргументов командной строки
def checkArgs(args):
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

# Получение пути к подсистемам в зависимости от указания пути и ОС
def getPathToFolder(args, folder_name, splitter):
    if args.sourcedirectory[-1] == splitter:
        path_to_folder = args.sourcedirectory+folder_name+splitter
    else:
        path_to_folder = args.sourcedirectory+splitter+folder_name+splitter

    return path_to_folder

# Получение наименование объектов метаданных в указанных подсистемах
def getMetadataName(subsystems_path, splitter):
    os.chdir(subsystems_path)
    # поиск файлов подсистем с заданным префиксом
    subsystems_folders = glob.glob("**"+splitter+args.parseprefix+"*.xml", recursive=True)

    set_metadata_name = set()
    list_metadata_name = []

    for subsystem_folder in subsystems_folders:
        for metadata_name in getObjects(subsystems_path+subsystem_folder):
            set_metadata_name.add(metadata_name)

    list_metadata_name = list(set_metadata_name)
    list_metadata_name.sort()

    return list_metadata_name

# Получение путей к bsl файлам для определенных метаданных
# def getBslFilesPath(list_metadata_name, source_path, full_path=False):
#     for metadata_name in list_metadata_name:
         
#         os.chdir(source_path+metadata_name)


########################################################################################################


# Получение парсера и разбор параметров командной строки
parser = createParser()
args = parser.parse_args()

# Проверка аргументов командной строки
checkArgs(args)

# Определение ОС Windows и сплиттера, для замены слешей в путях к файлам и папкам
# windows_os = True if sys.platform.find("window") != -1 else False
splitter = "\\" if sys.platform.find("window") != -1  else "/"

subsystems_path = getPathToFolder(args, "subsystems", splitter)

# Получение наименование объектов метаданных
list_metadata_name = getMetadataName(subsystems_path, splitter)

# set_bsl_files = set()

# for metadata in list_metadata:
#     for obj in getObjects(SUBSYSTEMS_PATH+file):
#         set_metadata.add(obj)

linenum = 1
for li in list_metadata_name:
    print(str(linenum)+". "+li)
    linenum = linenum + 1