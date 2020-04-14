import unittest
import os
import contextlib
import shutil
from io import StringIO
from bsl2sq.bslfinder import BslFinder


unittest.TestCase.maxDiff = None
ABS_PATH_TEST_CONF = os.path.abspath("tests/test_conf")
ABS_PATH_FIXTURE_SONAR_FILE = os.path.join(ABS_PATH_TEST_CONF, "fixture-sonar-project.properties")
ABS_PATH_FIXTURE_SONAR_STDOUT = os.path.join(ABS_PATH_TEST_CONF, "fixture_stdout")
ABS_PATH_TEMPLATE_SONAR_FILE = os.path.join(ABS_PATH_TEST_CONF, "template-sonar-project.properties")
ABS_PATH_TEMPLATE_FILL_SONAR_FILE = os.path.join(ABS_PATH_TEST_CONF, "template-fill-sonar-project.properties")
ABS_PATH_SONAR_FILE = os.path.join(ABS_PATH_TEST_CONF, "sonar-project.properties")
ABS_PATH_FILL_SONAR_FILE = os.path.join(ABS_PATH_TEST_CONF, "sonar-fill-project.properties")


def setUpModule():
    shutil.copyfile(ABS_PATH_TEMPLATE_SONAR_FILE, ABS_PATH_SONAR_FILE)
    shutil.copyfile(ABS_PATH_TEMPLATE_FILL_SONAR_FILE, ABS_PATH_FILL_SONAR_FILE)


def tearDownModule():
    os.remove(ABS_PATH_SONAR_FILE)
    os.remove(ABS_PATH_FILL_SONAR_FILE)


class TestBslFinder(unittest.TestCase):

    def setUp(self):

        with open(ABS_PATH_FIXTURE_SONAR_FILE, 'r', encoding='utf-8') as fsp:
            self.fixture_sp_list = fsp.read().splitlines()
            self.fixture_sp_list = [l.replace(", \\", "") for l in self.fixture_sp_list]

        with open(ABS_PATH_FIXTURE_SONAR_STDOUT, 'r', encoding='utf-8') as fsd:
            self.fixture_sd_list = fsd.read().splitlines()

        args_stdout = {
            'sourcedirectory': ABS_PATH_TEST_CONF,
            'parseprefix': "рн_ пс_",
            'file': "",
            'absolute': False,
            'unicode': True,
            'verbose': True
        }

        args_file = {
            'sourcedirectory': ABS_PATH_TEST_CONF,
            'parseprefix': "рн_ пс_",
            'file': ABS_PATH_SONAR_FILE,
            'absolute': False,
            'unicode': True,
            'verbose': True
        }

        args_fill_file = {
            'sourcedirectory': ABS_PATH_TEST_CONF,
            'parseprefix': "рн_ пс_",
            'file': ABS_PATH_FILL_SONAR_FILE,
            'absolute': False,
            'unicode': True,
            'verbose': True
        }

        self.bslfinder_stdout = BslFinder(args_stdout)
        self.bslfinder_file = BslFinder(args_file)
        self.bslfinder_fill_file = BslFinder(args_fill_file)

        self.subsytem_file_path = os.path.join(ABS_PATH_TEST_CONF, "Subsystems/рн_Супер.xml")

        self.test_string = "Проверка преобразования в символы unicode"
        self.count_get_subsystems_files_paths = 7
        self.count_get_objects_names_from_subsystem = 2
        self.count_get_list_metadata_name = 24
        self.count_get_bsl_files_paths = 63
        self.count_get_bsl_files_line = 6849

    def test_string_to_unicode(self):
        stu = self.bslfinder_stdout.string_to_unicode(self.test_string)
        patt = self.test_string.encode("unicode-escape").decode("utf-8")
        self.assertEqual(stu, patt)

    def test_string_to_nonunicode(self):
        self.bslfinder_stdout.args["unicode"] = False
        stu = self.bslfinder_stdout.string_to_unicode(self.test_string)
        patt = self.test_string
        self.assertEqual(stu, patt)

    def test_get_subsystems_files_paths(self):
        gsfp = self.bslfinder_stdout.get_subsystems_files_paths()
        self.assertIsInstance(gsfp, list)
        self.assertEqual(len(gsfp), self.count_get_subsystems_files_paths)

    def test_get_objects_names_from_subsystem(self):
        gonfs = self.bslfinder_stdout.get_objects_names_from_subsystem(self.subsytem_file_path)
        self.assertIsInstance(gonfs, set)
        self.assertEqual(len(gonfs), self.count_get_objects_names_from_subsystem)

    def test_get_list_metadata_name(self):
        glmn = self.bslfinder_stdout.get_list_metadata_name()
        self.assertIsInstance(glmn, list)
        self.assertEqual(len(glmn), self.count_get_list_metadata_name)

    def test_get_bsl_files_paths(self):
        gbfp = self.bslfinder_stdout.get_bsl_files_paths()
        self.assertIsInstance(gbfp, list)
        self.assertEqual(len(gbfp), self.count_get_bsl_files_paths)

    def test_get_bsl_files_line(self):
        gbfl = self.bslfinder_file.get_bsl_files_line()
        self.assertIsInstance(gbfl, str)
        self.assertEqual(len(gbfl), self.count_get_bsl_files_line)

    def test_write_bsl_line_to_file(self):
        self.bslfinder_file.write_bsl_line_to_files()
        with open(self.bslfinder_file.args["file"], 'r', encoding='utf-8') as sonar_properties_file_read:
            sonar_properties_list = sonar_properties_file_read.read().splitlines()
            sonar_properties_list = [l.replace(", \\", "") for l in sonar_properties_list]
            self.assertEqual(sorted(sonar_properties_list), sorted(self.fixture_sp_list))

    def test_write_bsl_line_to_fill_file(self):
        self.bslfinder_fill_file.write_bsl_line_to_files()
        with open(self.bslfinder_fill_file.args["file"], 'r', encoding='utf-8') as sonar_properties_file_read:
            sonar_properties_list = sonar_properties_file_read.read().splitlines()
            sonar_properties_list = [l.replace(", \\", "") for l in sonar_properties_list]
            self.assertEqual(sorted(sonar_properties_list), sorted(self.fixture_sp_list))

    def test_write_bsl_files_paths_to_stdout(self):

        temp_stdout = StringIO()

        with contextlib.redirect_stdout(temp_stdout):
            self.bslfinder_stdout.write_bsl_files_paths_to_stdout()

        output_list = temp_stdout.getvalue().splitlines()
        self.assertEqual(sorted(output_list), sorted(self.fixture_sd_list))


if __name__ == "__main__":
    unittest.main()
