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

    def test_create_parser(self):
        parser = self.cliparser.create_parser()
        self.assertIsInstance(parser, argparse.ArgumentParser)
        self.assertEqual(len(parser._actions), self.count_argument)

    def test_check_args_stdout(self):

        args = argparse.Namespace()

        args.sourcedirectory = ABS_PATH_TEMPLATE_SONAR_FILE
        args.parseprefix = "рн_"
        args.file = ""
        args.absolute = False
        args.unicode = True
        args.verbose = True

        temp_stdout = StringIO()

        with contextlib.redirect_stdout(temp_stdout):
            self.cliparser.check_args(args)

        output = temp_stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_check_args_file(self):

        args = argparse.Namespace()

        args.sourcedirectory = ABS_PATH_TEMPLATE_SONAR_FILE
        args.parseprefix = "рн_"
        args.file = ABS_PATH_FIXTURE_SONAR_FILE
        args.absolute = True
        args.unicode = True
        args.verbose = True

        temp_stdout = StringIO()

        with contextlib.redirect_stdout(temp_stdout):
            self.cliparser.check_args(args)

        output = temp_stdout.getvalue().strip()
        self.assertEqual(output, "")


if __name__ == "__main__":
    unittest.main()
