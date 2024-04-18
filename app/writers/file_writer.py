import unicodecsv as csv

from PyQt6.QtCore import QObject


class FileWriter(QObject):
    def __init__(self):
        super(FileWriter, self).__init__()
        
        self.__filename = str()
        self.__file = None
        self.__writer = None

    def set_file(self, filename: str):
        self.__filename = filename

        self.__file = open(self.__filename, "ab")

    def close_file(self):
        if self.__file is not None:
            self.__file.close()
        
        self.__writer = None

    def add_data(self, data: dict):
        if (self.__writer is None) and (self.__file is not None):
            self.__writer = csv.DictWriter(
                self.__file, fieldnames=data.keys(),
                delimiter=";"
            )
            self.__writer.writeheader()

        if self.__writer is not None:
            data_with_comma_decimal = dict()
            for key, value in data.items():
                data_with_comma_decimal[key] = str(value).replace(".", ",")

            self.__writer.writerow(data_with_comma_decimal)