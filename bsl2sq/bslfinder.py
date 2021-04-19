import glob
import os
import re
import xml.dom.minidom as minidom
import logging

logging.basicConfig(format=u'[%(asctime)s]  %(message)s', level=logging.INFO)


class BslFinder:

    KEYWORD_SONAR_INCLUSION = "sonar.inclusions="
    KEYWORD_INCL_LINE_END = "$inclusions_end"
    KEYWORD_INCL_LINE = "$inclusions_line"

    def __init__(self, args) -> None:
        super().__init__()
        self.args = args
        self.root_subsystems_path = os.path.join(args["sourcedirectory"], "Subsystems")

    def string_to_unicode(self, string) -> str:
        """ Преобразование строки в unicode символы
        """
        if self.args["unicode"]:
            return string.encode("unicode-escape").decode("utf-8")
        else:
            return string

    def get_subsystems_files_paths(self) -> list:
        """ Получение списка .xml файлов подсистем конфигурации по префиксам
        """

        os.chdir(self.root_subsystems_path)
        subsystems_files_paths = []

        # Перебор всех переданных префиксов подсистем
        for prfx in self.args["parseprefix"].split(' '):
            # поиск относительного пути файлов подсистем с заданным префиксом
            subsystems_files_paths.extend(glob.glob(os.path.join("**", prfx + "*.xml"), recursive=True))

        if self.args["verbose"]:
            logging.info(f">>> Найдено подсистем для анализа: {len(subsystems_files_paths)}")

        return subsystems_files_paths

    def get_objects_names_from_subsystem(self, file) -> set:
        """ Парсинг .xml файла подсистемы конфигурации,
            для получения списка объектов в этой подсистеме
        """

        doc = minidom.parse(file)

        subsys_tag = doc.getElementsByTagName("MetaDataObject")[0].getElementsByTagName("Subsystem")[0]
        content_tag = subsys_tag.getElementsByTagName("Properties")[0].getElementsByTagName("Content")[0]

        sub_items = content_tag.getElementsByTagName("xr:Item")

        # Маска поиска guid удаленных объектов, которые остались в подсистемах, чтобы их исключить
        mask = "[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
        set_metadata_names = set()

        for item in sub_items:
            if len(item.childNodes) == 0:
                continue
            obj = item.childNodes[0].data
            # Проверка результата, что он является путем к объекту, а не guid
            if not re.match(mask, obj):
                set_metadata_names.add(item.childNodes[0].data)

        return set_metadata_names

    def get_list_metadata_name(self) -> list:
        """ Получение списка наименований объектов метаданных,
            в подсистемах конфигурации по префиксам
        """

        subsystems_files_paths = self.get_subsystems_files_paths()

        set_metadata_name = set()
        list_metadata_name = []

        for sub_path in subsystems_files_paths:

            # Вывод подробного лога выполнения
            if self.args["verbose"]:
                logging.info(sub_path)

            for metadata_name in self.get_objects_names_from_subsystem(sub_path):
                set_metadata_name.add(metadata_name)

        list_metadata_name = list(set_metadata_name)
        list_metadata_name.sort()

        # Вывод подробного лога выполнения
        if self.args["verbose"]:
            logging.info(f">>> Найдено объектов для анализа: {len(list_metadata_name)}")

        return list_metadata_name

    def get_bsl_files_paths(self) -> list:
        """ Получение списка путей bsl файлов,
            в подсистемах конфигурации, по которым проводится поиск
        """

        list_metadata_name = self.get_list_metadata_name()

        list_bsl_files_paths = []

        # Получение путей к bsl файлам для определенных метаданных
        for metadata_name in list_metadata_name:

            metadata_type_name = metadata_name[:metadata_name.find(".")] + "s"
            metadata_only_name = metadata_name[metadata_name.find(".") + 1:]
            metadata_rel_path = os.path.join(metadata_type_name, metadata_only_name)
            path_to_folder = os.path.join(self.args["sourcedirectory"], metadata_rel_path)

            if not os.path.exists(path_to_folder):
                continue

            os.chdir(path_to_folder)
            # поиск файлов подсистем с заданным префиксом
            bsl_files = glob.glob(os.path.join("**", "*.bsl"), recursive=True)
            # Базовая часть путу для bsl файла (абсолютная или относительно корня конфигурации)
            base_path = path_to_folder if self.args["absolute"] else metadata_rel_path

            # Преобразование путей файлов для добавление базовой части и двойных слешей в путях при работе в ОС Windows
            bsl_files = [os.path.join(base_path, bsl_file).replace("\\", "/") for bsl_file in bsl_files]

            list_bsl_files_paths.extend(bsl_files)

        # Вывод подробного лога выполнения
        if self.args["verbose"]:
            logging.info(f">>> Количество bsl модулей для проверки: {len(list_bsl_files_paths)}")

        return list_bsl_files_paths

    def get_bsl_files_line(self) -> str:
        """ Получение строки с bsl файлами,
            для подстановки в шаблон файла для sonarqube или АП
        """

        list_bsl_files_paths = self.get_bsl_files_paths()

        # Преобразование кодировки кириллических символов в юникод
        list_bsl_files_paths = list(map(self.string_to_unicode, list_bsl_files_paths))

        line_bsl_files = ""

        end_line = ", \\\n"
        end_line_last_line = "\n" + self.KEYWORD_INCL_LINE_END

        for bsl_file_path in list_bsl_files_paths:
            line_bsl_files = line_bsl_files + bsl_file_path + end_line

        last_end_line_index = len(line_bsl_files) - len(end_line)
        line_bsl_files = line_bsl_files[:last_end_line_index] + end_line_last_line

        return line_bsl_files

    def write_bsl_line_to_files(self) -> None:
        """ Запись строки с bsl файлами для проверки
            в указанные файлы с определенным форматом
        """

        line_bsl_files = self.get_bsl_files_line()

        with open(self.args["file"], 'r', encoding='utf-8') as sonar_properties_file_read:
            sonar_properties_text = sonar_properties_file_read.read()
            start_sublen = sonar_properties_text.find(self.KEYWORD_SONAR_INCLUSION)
            end_sublen = sonar_properties_text.find(self.KEYWORD_INCL_LINE_END)
            if end_sublen != -1:
                f_part_text = sonar_properties_text[:start_sublen + len(self.KEYWORD_SONAR_INCLUSION)]
                e_part_text = sonar_properties_text[end_sublen + len(self.KEYWORD_INCL_LINE_END):]
                sonar_properties_text = f_part_text + self.KEYWORD_INCL_LINE + e_part_text
        with open(self.args["file"], 'w', encoding='utf-8') as sonar_properties_file_write:
            sonar_properties_file_write.write(
                sonar_properties_text.replace(self.KEYWORD_INCL_LINE, line_bsl_files))

    def write_bsl_files_paths_to_stdout(self) -> None:
        """ Вывод списка объектов с bsl файлами для проверки
            в стандартный поток вывода
        """
        list_bsl_files_paths = self.get_bsl_files_paths()

        # Преобразование кодировки кириллических символов в юникод если необходимо
        list_bsl_files_paths = list(map(self.string_to_unicode, list_bsl_files_paths))

        for li in list_bsl_files_paths:
            print(li)

    def data_to_sq(self) -> None:
        """ Вывод списка объектов с bsl файлами для проверки
            в различные точки вывода
        """

        if len(self.args["file"]):
            self.write_bsl_line_to_files()
        else:
            self.write_bsl_files_paths_to_stdout()
