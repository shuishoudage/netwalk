import unittest
from netwalk.utils import reader
from parameterized import parameterized


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
