import unittest
import argparse  # Import the argparse module
from whatsapp_converter import parse


class TestParse(unittest.TestCase):
    def test_parse_with_valid_line(self):
        # Test parse function with a valid line
        line = "17/05/2021, 12:50 - Vijaya: Hey! This is Vijaya"
        local_args = argparse.Namespace(debug=False, verbose=False)
        result = parse(line, local_args)

        # Assert the output of the parse function
        self.assertEqual(result, ['new', '2021-05-17 12:50', '2021-05-17', '12:50', 'Vijaya', 'Hey! This is Vijaya'])

    def test_parse_with_valid_line(self):
        # Test parse function with a valid line
        line = "21/12/16, 10:50:12 PM: Neha Wipro: Awsum"
        local_args = argparse.Namespace(debug=False, verbose=False)
        result = parse(line, local_args)

        # Assert the output of the parse function
        self.assertEqual(result, ['new', '2016-12-21 22:50', '2016-12-21', '22:50', 'Neha Wipro', 'Awsum'])

    def test_parse_with_empty_line(self):
        # Test parse function with an empty line
        line = "\n"
        local_args = argparse.Namespace(debug=False, verbose=False)
        result = parse(line, local_args)

        # Assert the output of the parse function
        self.assertEqual(result, ['empty', '', '', '', '', ''])

if __name__ == '__main__':
    unittest.main()