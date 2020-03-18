import argparse
import glob
import os
import re
import sys
import xml.dom.minidom as minidom
from version import __version__


KEYWORD_SONAR_INCLUSION = "sonar.inclusions="
KEYWORD_INCL_LINE_END = "$inclusions_end"
KEYWORD_INCL_LINE = "$inclusions_line"


def create_parser():
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
                        help='в случае указания флага будут выгружаться все кириллические символы в символах unicode')
    parser.add_argument('-F', '--accfile', type=str, default="",
                        help='полный путь к файлу, в который будет выполняться \
                              выгрузка путей объектов метаданных для проверки в АПК')
    parser.add_argument('-v', '--verbose', action='store_const', const=True, default=False,
                        help='выводить описание выполняемых операций')
    parser.add_argument('-V', '--version', action='version', version=__version__,
                        help='вывести номер версии')

    return parser


def check_args(args):
    # Процедура проверки аргументов командной строки
    # Проверка существования указанной папки

    if not os.path.exists(args.sourcedirectory):
        print(args.sourcedirectory + " - папка не существует")
        sys.exit()
    # Проверка, что по указанному пути находится папка
    if not os.path.isdir(args.sourcedirectory):
        print(args.sourcedirectory + " - это не папка")
        sys.exit()
    # Проверка указания не пустого префикса для подсистем
    if len(args.parseprefix) == 0:
        print("необходимо указать не пустой префикс")
        sys.exit()
    # Проверка, что по указанному пути находится папка
    if len(args.file) != 0 and not os.path.exists(args.file):
        print("файл sonar-project.properties по указанному пути не найден")
        sys.exit()

    # Вывод подробного лога выполнения
    if args.verbose:
        print(f">>> Абсолютный путь к исходным файлам проекта: {os.path.abspath(args.sourcedirectory)}")
        print(f">>> Абсолютный путь к исходным файлу sonar-project.properties: {os.path.abspath(args.file)}")


def get_objects(file):
    # Парсинг xml файлов подсистем, для получения списка объектов
    doc = minidom.parse(file)
    subsys_tag = doc.getElementsByTagName("MetaDataObject")[0].getElementsByTagName("Subsystem")[0]
    content_tag = subsys_tag.getElementsByTagName("Properties")[0].getElementsByTagName("Content")[0]
    sub_items = content_tag.getElementsByTagName("xr:Item")
    # Маска поиска guid удаленных объектов, которые остались в подсистемах, чтобы их исключить
    mask = "[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
    metadata = set()
    for item in sub_items:
        obj = item.childNodes[0].data
        # Проверка результата, что он является путем к объекту, а не guid
        if not re.match(mask, obj):
            metadata.add(item.childNodes[0].data)
    return metadata


def get_metadata_name(subsystems_path):
    # Получение наименование объектов метаданных в указанных подсистемах
    os.chdir(subsystems_path)
    subsystems_folders = []

    # Перебор всех переданных префиксов подсистем
    for prfx in args.parseprefix.split(' '):
        # поиск файлов подсистем с заданным префиксом
        subsystems_folders.extend(glob.glob(os.path.join("**", prfx + "*.xml"), recursive=True))

    if args.verbose:
        print(f">>> Найдено подсистем для анализа: {len(subsystems_folders)}")
        count = 1

    set_metadata_name = set()
    list_metadata_name = []

    for subsystem_folder in subsystems_folders:
        sf_path = os.path.join(subsystems_path, subsystem_folder)

        # Вывод подробного лога выполнения
        if args.verbose:
            print(f"{count}. {sf_path}")
            count = count + 1

        for metadata_name in get_objects(sf_path):
            set_metadata_name.add(metadata_name)

    list_metadata_name = list(set_metadata_name)
    list_metadata_name.sort()

    # Вывод подробного лога выполнения
    if args.verbose:
        print(f">>> Найдено объектов для анализа: {len(list_metadata_name)}")

    return list_metadata_name


def get_bsl_files_path(list_bsl_files_acc, list_bsl_files_sc, list_metadata_name, source_path,
                       full_path=False, accfile=''):
    # Получение путей к bsl файлам для определенных метаданных
    for metadata_name in list_metadata_name:
        metadata_type_name = metadata_name[:metadata_name.find(".")] + "s"
        metadata_only_name = metadata_name[metadata_name.find(".") + 1:]
        path_to_folder = os.path.join(args.sourcedirectory, metadata_type_name, metadata_only_name)

        if not os.path.exists(path_to_folder):
            continue

        os.chdir(path_to_folder)
        # поиск файлов подсистем с заданным префиксом
        bsl_files = glob.glob(os.path.join("**", "*.bsl"), recursive=True)

        for file in bsl_files:
            append_to_list_bsl_files_sc(file, full_path, path_to_folder, metadata_type_name, metadata_only_name)
            if len(accfile) != 0:
                append_to_list_bsl_files_acc(file, full_path, path_to_folder, metadata_type_name, metadata_only_name)


def append_to_list_bsl_files_sc(file, full_path, path_to_folder, metadata_type_name, metadata_only_name):
    if full_path:
        bsl_path_sc = os.path.join("**", path_to_folder, file)
    else:
        bsl_path_sc = os.path.join("**", metadata_type_name, metadata_only_name, file)

    bsl_path_sc = bsl_path_sc.replace("\\", "/")
    bsl_path_sc = bsl_path_sc.encode("unicode-escape").decode("utf-8") if args.unicode else bsl_path_sc
    list_bsl_files_sc.append(bsl_path_sc)


def append_to_list_bsl_files_acc(file, full_path, path_to_folder, metadata_type_name, metadata_only_name):
    if full_path:
        bsl_path_acc = os.path.join(path_to_folder, file)
    else:
        bsl_path_acc = os.path.join(metadata_type_name, metadata_only_name, file)

    bsl_path_acc = bsl_path_acc.replace("\\", "/")
    list_bsl_files_acc.append(bsl_path_acc)


def get_bsl_files_line(list_bsl_files, is_acc_files_line=False):
    # Получение строки с bsl файлами для подстановки в шаблон
    count_bsl_files = len(list_bsl_files)
    counter = 1
    line_bsl_files = ""
    end_line = "\n" if is_acc_files_line else (", \\" + "\n")
    end_line_last_line = "" if is_acc_files_line else ("\n" + "#$inclusions_line_end")

    for bsl_file_path in list_bsl_files:
        if counter != count_bsl_files:
            line_bsl_files = line_bsl_files + bsl_file_path + end_line
        else:
            line_bsl_files = line_bsl_files + bsl_file_path + end_line_last_line

    counter = counter + 1

    return line_bsl_files


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    check_args(args)
    subsystems_path = os.path.join(args.sourcedirectory, "subsystems")
    list_metadata_name = get_metadata_name(subsystems_path)

    # Список файлов проверки для sonar-scanner
    list_bsl_files_sc = []
    # Список файлов проверки для АПК
    list_bsl_files_acc = []

    # Заполнение списков файлов
    get_bsl_files_path(list_bsl_files_acc, list_bsl_files_sc, list_metadata_name,
                       args.sourcedirectory, args.absolute, args.accfile)

    # Вывод подробного лога выполнения
    if args.verbose:
        print(f">>> Количество bsl модулей для проверки sonar-project.properties: {len(list_bsl_files_acc)}")
        print(f">>> Количество bsl модулей для проверки в АПК: {len(list_bsl_files_sc)}")

    if len(args.file):
        bsl_files_line = get_bsl_files_line(list_bsl_files_sc)
        with open(args.file, 'r', encoding='utf-8') as sonar_properties_file_read:
            sonar_properties_text = sonar_properties_file_read.read()
            start_sublen = sonar_properties_text.find(KEYWORD_SONAR_INCLUSION)
            end_sublen = sonar_properties_text.find(KEYWORD_INCL_LINE_END)
            if end_sublen != -1:
                f_part_text = sonar_properties_text[:start_sublen + len(KEYWORD_SONAR_INCLUSION)]
                e_part_text = sonar_properties_text[end_sublen + len(KEYWORD_INCL_LINE_END):]
                sonar_properties_text = f_part_text + KEYWORD_INCL_LINE + e_part_text
        with open(args.file, 'w', encoding='utf-8') as sonar_properties_file_write:
            sonar_properties_file_write.write(
                sonar_properties_text.replace(KEYWORD_INCL_LINE, bsl_files_line + KEYWORD_INCL_LINE_END))
    else:
        for li in list_bsl_files_sc:
            print(li)

    if len(args.accfile) != 0:
        with open(args.accfile, 'w', encoding='utf-8') as acc_file_write:
            acc_file_write.write(get_bsl_files_line(list_bsl_files_acc, True))
