import unittest

class TestCheckArgs(unittest.TestCase):

    def test_simple_case(self):
        self.assertEqual(9, 9, 'it\'s okay')

if __name__ == "__main__":
    unittest.main()