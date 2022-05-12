import csv

import pandas as pd

from pdf.Util import check_path


class Csv:
    def __init__(self, path, delimiter=',', create=False):
        self.path = path
        self.file_handle = self._init_file_handle(path, create)
        self.delimiter = delimiter

    def _init_file_handle(self, path, create):
        if create:
            return open(path, 'w')
        elif check_path(path, extension='.csv'):
            return open(path)
        else:
            raise OSError('bad file format')

    def get_file_handle(self):
        return self.file_handle

    def process_first_n_lines(self, n):
        csv_reader = csv.reader(self.file_handle, delimiter=self.delimiter)
        line_count = 0
        csv_dict = {}
        for row in csv_reader:
            if line_count < n:
                csv_dict[row[0]] = row[1]
                line_count += 1
            else:
                return csv_dict

    # def create_pd_from_csv(self, skip_rows, converted_dict=None):
    #     csv_df = pd.read_csv(self.path, skiprows=skip_rows, converters=converted_dict)
    #     return csv_df
    def create_pd_from_csv(self, **kwargs):
        csv_df = pd.read_csv(self.path, **kwargs)
        return csv_df

    def create_csv_from_pd(self, df, **kwargs):
        df.to_csv(self.path, **kwargs)

        # writer = csv.writer(self.file_handle)
        # for key, value in csv_dict.items():
        #     writer.writerow([key, value])
