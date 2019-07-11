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
                        help='полный путь к файлу sonar-project.properties, в который будет выполняться выгрузка путей объектов метаданных на место переменной $inclusions_line')
    parser.add_argument('-a', '--absolute', action='store_const', const=True, default=False,
                        help='в случае указания флага будут выгружаться полные пути к файлам. без флага только относительные пути')
    parser.add_argument('-b', '--bytes', action='store_const', const=True, default=False,
                        help='в случае указания флага будут выгружаться все кириллические символы в байтах')                        

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
    # Проверка, что по указанному пути находится папка
    if len(args.file) != 0:
        if not os.path.exists(args.file):
            print("файл sonar-project.properties по указанному пути не найден")
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

# Получение наименование объектов метаданных в указанных подсистемах
def getMetadataName(subsystems_path):
    os.chdir(subsystems_path)
    # поиск файлов подсистем с заданным префиксом
    subsystems_folders = glob.glob(os.path.join("**", args.parseprefix+"*.xml"), recursive=True)

    set_metadata_name = set()
    list_metadata_name = []

    for subsystem_folder in subsystems_folders:
        for metadata_name in getObjects(os.path.join(subsystems_path, subsystem_folder)):
            set_metadata_name.add(metadata_name)

    list_metadata_name = list(set_metadata_name)
    list_metadata_name.sort()

    return list_metadata_name

# Получение путей к bsl файлам для определенных метаданных
def getBslFilesPath(list_metadata_name, source_path, full_path=False):
    list_bsl_files = []
    for metadata_name in list_metadata_name:
        metadata_type_name = metadata_name[:metadata_name.find(".")]+"s"
        metadata_only_name = metadata_name[metadata_name.find(".")+1:]
        path_to_folder = os.path.join(args.sourcedirectory, metadata_type_name, metadata_only_name)

        if not os.path.exists(path_to_folder): continue

        os.chdir(path_to_folder)
        # поиск файлов подсистем с заданным префиксом
        bsl_files = glob.glob(os.path.join("**", "*.bsl"), recursive=True)

        for file in bsl_files:
            if full_path:
                bsl_path = os.path.join(path_to_folder, file)
            else:
                bsl_path = os.path.join(metadata_type_name, metadata_only_name, file)
            
            list_bsl_files.append(bsl_path)
            
    return list_bsl_files

# Получение строки с bsl файлами для подстановки в шаблон
def getBslFilesLine(list_bsl_files, unicode_bytes=False):
    count_bsl_files = len(list_bsl_files)
    counter = 1
    line_bsl_files = ""
    for bsl_file_path in list_bsl_files:
        if counter != count_bsl_files:
            line_bsl_files = line_bsl_files + bsl_file_path +", \\"+"\n"
        else:
            line_bsl_files = line_bsl_files + bsl_file_path 
        counter = counter + 1

    return line_bsl_files

########################################################################################################

# TODO: Сделать процедуру со списком соответствия кириллице unicode номерам символов

# Получение парсера и разбор параметров командной строки
parser = createParser()
args = parser.parse_args()

checkArgs(args)

subsystems_path = os.path.join(args.sourcedirectory, "subsystems")

list_metadata_name = getMetadataName(subsystems_path)

# TODO: Сделать подмену кириллических символов на номера unicode символов по списку из функции
list_bsl_files = getBslFilesPath(list_metadata_name, args.sourcedirectory, args.absolute)

if len(args.file):
    bsl_files_line = getBslFilesLine(list_bsl_files)
    with open(args.file,'r', encoding='utf-8') as sonar_properties_file_read:
        sonar_properties_text = sonar_properties_file_read.read()
    with open(args.file,'w', encoding='utf-8') as sonar_properties_file_write:
        sonar_properties_file_write.write(sonar_properties_text.replace("$inclusions_line", bsl_files_line))
else:
    for li in list_bsl_files:
        print(li) 