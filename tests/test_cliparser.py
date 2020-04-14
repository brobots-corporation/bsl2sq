import unittest
import argparse
import contextlib
import os
from io import StringIO
from bsl2sq.cliparser import CliParser

ABS_PATH_TEMPLATE_SONAR_FILE = os.path.abspath("tests/test_conf")
ABS_PATH_FIXTURE_SONAR_FILE = os.path.join(ABS_PATH_TEMPLATE_SONAR_FILE, "template-sonar-project.properties")


class TestCliParser(unittest.TestCase):

    def setUp(self):
        self.cliparser = CliParser()
        self.count_argument = 8

        args = argparse.Namespace()

        args.sourcedirectory = ABS_PATH_TEMPLATE_SONAR_FILE
        args.parseprefix = "рн_"
        args.file = ABS_PATH_FIXTURE_SONAR_FILE
        args.absolute = True
        args.unicode = True
        args.verbose = True

        self.args = args

    def test_create_parser(self):
        parser = self.cliparser.create_parser()
        self.assertIsInstance(parser, argparse.ArgumentParser)
        self.assertEqual(len(parser._actions), self.count_argument)

    def test_check_args_stdout(self):

        self.args.file = ""

        temp_stdout = StringIO()

        with contextlib.redirect_stdout(temp_stdout):
            self.cliparser.check_args(self.args)

        output = temp_stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_check_args_file(self):

        temp_stdout = StringIO()

        with contextlib.redirect_stdout(temp_stdout):
            self.cliparser.check_args(self.args)

        output = temp_stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_check_args_dir_exist_error(self):

        self.args.sourcedirectory = "/dummy_folder"

        check_msg = self.args.sourcedirectory + " - папка не существует\n" + self.args.sourcedirectory \
            + " - это не папка"

        temp_stdout = StringIO()

        with contextlib.redirect_stdout(temp_stdout):
            self.cliparser.check_args(self.args)

        output = temp_stdout.getvalue().strip()
        self.assertEqual(output, check_msg)

    def test_check_args_prefix_exist_error(self):

        self.args.parseprefix = ""

        check_msg = "необходимо указать не пустой префикс"

        temp_stdout = StringIO()

        with contextlib.redirect_stdout(temp_stdout):
            self.cliparser.check_args(self.args)

        output = temp_stdout.getvalue().strip()
        self.assertEqual(output, check_msg)

    def test_check_args_file_exist_error(self):

        self.args.file = "dummy_template-sonar-project.properties"

        check_msg = "файл sonar-project.properties по указанному пути не найден"

        temp_stdout = StringIO()

        with contextlib.redirect_stdout(temp_stdout):
            self.cliparser.check_args(self.args)

        output = temp_stdout.getvalue().strip()
        self.assertEqual(output, check_msg)


if __name__ == "__main__":
    unittest.main()
