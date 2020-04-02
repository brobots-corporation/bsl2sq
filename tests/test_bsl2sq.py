import unittest
from ..bsl2sq.cliparser import CliParser
from ..bsl2sq.bslfinder import BslFinder

# import bsl2sq


class TestCheckArgs(unittest.TestCase):

    def setUp(self):
        self.cliparser = CliParser()
        self.bslfinder = BslFinder()

    # def test_args(self):
    #     self.assertEqual()

    def test_simple_case(self):
        self.assertEqual(9, 9, 'it\'s okay')


if __name__ == "__main__":
    unittest.main()
