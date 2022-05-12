import os
import sys
from pathlib import Path
from os.path import isfile, join
import re

import pdfplumber
import fitz

from pdf.Util import check_path


def replace_chars(string, pattern, repl=" "):
    return re.sub(pattern, repl, string)


class Pdf:
    forbidden_chars = "[\\/\:\*\?\"\<\>\|]"
    metadata_keys = ['title', 'keywords', 'title', 'subject']

    def __init__(self, path, method):
        if method == "fitz":
            self.method = fitz
        elif method == "pdfplumber":
            self.method = pdfplumber
        self.file_handle = self._init_file_handle(path)

    def __del__(self):
        try:
            self.file_handle.close()
        except:
            pass

    def get_raw_metadata(self):
        return self.file_handle.metadata

    def get_metadata(self):
        metadata = self.get_raw_metadata()

        # convert to ascii
        self._convert_string(metadata)

        # clean strings
        self._clean_strings(metadata)
        return metadata

    def _init_file_handle(self, path):
        '''
        :param path:
        :param method:
                   - "fitz" - PyMuPDF
                   - "pdfplumber"  - pdfplumber:
        :return:
        '''
        if check_path(path, extension='.pdf'):
            return self.method.open(path)
        else:
            raise OSError('bad file format')

    def get_file_handle(self):
        return self.file_handle

    def _convert_string(self, metadata):
        '''
        convert string to ascii
        :return:
        '''
        metadata.update(
            (key, metadata[key].encode("ascii", "replace").decode()) for key in metadata.keys() & self.metadata_keys)
        # {key: metadata[key].encode("ascii", "replace").decode() for key in metadata.keys()}

    def _clean_strings(self, metadata):
        # check keywords \r\n -> ;
        metadata['keywords'] = replace_chars(metadata['keywords'].rstrip(), "\r\n", "; ")

        # title
        metadata['title'] = replace_chars(metadata['title'], self.forbidden_chars)

        # author
        metadata['author'] = replace_chars(metadata['author'], self.forbidden_chars)

        # importance - subject
        metadata['subject'] = replace_chars(metadata['subject'], self.forbidden_chars)
        metadata['subject'] = replace_chars(metadata['subject'], "[^+-=]", "")
        # importance = re.sub("[^+-=]", "", metadata['subject'])
