import unittest
import argparse
import contextlib
import os
from io import StringIO
from bsl2sq.cliparser import CliParser

abs_path_test_conf = os.path.abspath("tests/test_conf")


class TestCliParser(unittest.TestCase):

    def setUp(self):
        self.cliparser = CliParser()
        os.chdir(abs_path_test_conf)

    def test_create_parser(self):
        parser = self.cliparser.create_parser()
        self.assertIsInstance(parser, argparse.ArgumentParser)
        self.assertEqual(len(parser._actions), 8)

    def test_check_args_stdout(self):

        args = argparse.Namespace()

        args.sourcedirectory = abs_path_test_conf
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

        args.sourcedirectory = abs_path_test_conf
        args.parseprefix = "рн_"
        args.file = os.path.join(abs_path_test_conf, "sonar-project.properties")
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
