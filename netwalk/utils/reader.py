import itertools
import os

"""This class is mainly to read text data files like tab, space or comma
separated file format

Returns
-------
data: generator
    a generator that yields data line by line from the give file
header: list
    a list that represent the header fields

Raises
------
e: IOError
    [raise when provided file name not exists]
e: PermissonError
    [raised when no reading permission]

Examples
--------
>> txtReader = FileReader("file_loc", header=True)
>> txtReader.get_header()
>> for line in txtReader.get_data():
>>      print(line)
"""


class FileReader:
    def __init__(self, file_name: str,
                 delimiter: str = ' ', header: bool = False):
        """create FileReader object, with default delimiter as space and assume
        without header presents in given file

        Parameters
        ----------
        file_name : str
            the given file location
        delimiter : str, default ' '
            the delimiter of given file, can be space, comma or tab
        header : bool, default False
            indicates if header is presented on the given file
        """
        try:
            self.fd = open(file_name, 'r')
        except IOError as e:
            raise e
        except PermissionError as e:
            raise e
        if delimiter not in ", " + os.linesep:
            raise ValueError("for delimiter, only space, comma, tab supported")
        self.delimiter = delimiter
        self.header = header

    def get_data(self):
        """
        get the data body, if header presents, skip header
        """
        for line in itertools.islice(self.fd, self.header, None):
            fields = list(map(str.strip, line.rstrip().split(self.delimiter)))
            yield fields

    def get_header(self):
        """
        return the header field of give file
        """
        return list(map(str.strip,
                        self.fd.readline().rstrip().split(self.delimiter)))

    def __del__(self):
        """
        destructor for closing opened resources
        """
        if hasattr(self, 'fd'):
            self.fd.close()
