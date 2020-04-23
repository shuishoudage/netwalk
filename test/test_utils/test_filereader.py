import unittest
from netwalk.utils import reader
from parameterized import parameterized
from unittest.mock import patch
import os


class FileReaderTest(unittest.TestCase):
    def setUp(self):
        self.common_path = "test/stub_files/"

    @parameterized.expand([
        ("unknown", ' ', IOError),
        ("not_readable.txt", ' ', PermissionError),
        ("withheader.txt", '.', ValueError)
    ])
    def test_constructor_exceptions(self, arg, delimiter, expected):
        with self.assertRaises(expected):
            _ = reader.FileReader(self.common_path + arg, delimiter=delimiter)

    @parameterized.expand([
        ("withheader.txt", True, ' ', ['name', 'height', 'width']),
        ("withoutheader.txt", False, ' ', ['abc', '10', '20', '30']),
        ("withheader.csv", True, ',', ['name', 'height', 'width']),
        ("withoutheader.csv", False, ',', ['abc', '10', '20', '30']),
    ])
    def test_file_with_header(self, arg, header, delimiter, expected):
        header = reader.FileReader(
            self.common_path + arg,
            delimiter=delimiter,
            header=header).get_header()
        self.assertListEqual(expected, header)

    @parameterized.expand([
        ('mock_non_exits_file.txt', ' ', None, IOError),
        ('mock_non_readable.txt', ' ', None, PermissionError),
        ('mock_with_wrong_delimiter.txt', '.',
         'name, height, width' + os.linesep + 'abc, 15, 20', ValueError)
    ])
    def test_mock_no_exit_file(self, file_name, delimiter, data, expected):
        with patch('netwalk.utils.reader.FileReader', side_effect=expected):
            with self.assertRaises(expected):
                _ = reader.FileReader(file_name, delimiter=delimiter)
