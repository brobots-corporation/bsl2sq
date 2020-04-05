import unittest
import os
import contextlib
from io import StringIO
from bsl2sq.bslfinder import BslFinder

unittest.TestCase.maxDiff = None
abs_path_test_conf = os.path.abspath("tests/test_conf")


class TestBslFinder(unittest.TestCase):

    def setUp(self):

        with open(os.path.join(abs_path_test_conf, "fixture-sonar-project.properties"), 'r', encoding='utf-8') as fsp:
            self.fixture_sp = fsp.read()

        with open(os.path.join(abs_path_test_conf, "fixture_stdout"), 'r', encoding='utf-8') as fsd:
            self.fixture_sd = fsd.read()

        args_stdout = {
            'sourcedirectory': abs_path_test_conf,
            'parseprefix': "рн_ пс_",
            'file': "",
            'absolute': False,
            'unicode': True,
            'verbose': True
        }

        args_file = {
            'sourcedirectory': abs_path_test_conf,
            'parseprefix': "рн_ пс_",
            'file': os.path.join(abs_path_test_conf, "sonar-project.properties"),
            'absolute': False,
            'unicode': True,
            'verbose': True
        }

        self.bslfinder_stdout = BslFinder(args_stdout)
        self.bslfinder_file = BslFinder(args_file)

        self.subsytem_file_path = os.path.join(abs_path_test_conf, "Subsystems/рн_Супер.xml")

        self.count_get_subsystems_files_paths = 7
        self.count_get_objects_names_from_subsystem = 2
        self.count_get_list_metadata_name = 24
        self.count_get_bsl_files_paths = 63
        self.count_get_bsl_files_line = 6849

        os.chdir(abs_path_test_conf)

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

    def test_write_bsl_line_to_files(self):
        self.bslfinder_file.write_bsl_line_to_files()
        with open(self.bslfinder_file.args["file"], 'r', encoding='utf-8') as sonar_properties_file_read:
            sonar_properties_text = sonar_properties_file_read.read()
            self.assertEqual(sonar_properties_text, self.fixture_sp)

    def test_write_bsl_files_paths_to_stdout(self):

        temp_stdout = StringIO()

        with contextlib.redirect_stdout(temp_stdout):
            self.bslfinder_stdout.write_bsl_files_paths_to_stdout()

        output = temp_stdout.getvalue().strip()
        self.assertEqual(output, self.fixture_sd)


if __name__ == "__main__":
    unittest.main()