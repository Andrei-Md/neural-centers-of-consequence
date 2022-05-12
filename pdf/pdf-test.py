import sys

import pdfplumber
import os
from pathlib import Path
import fitz

from os import listdir
from os.path import isfile, join

## borb
import typing
from borb.pdf.document.document import Document
from borb.pdf.pdf import PDF
##

def check_path(path):
    if not path.exists():
        print("Oops, file doesn't exist!")
        sys.exit()
    else:
        print(path)


def get_file_handle(path, method):
    '''
    :param path:
    :param method:
               - "fitz" - PyMuPDF
               - "pdfplumber"  - pdfplumber:
    :return:
    '''
    file = method.open(path)
    return file


def get_metadata(file):
    return file.metadata


def rename_files(folder_path, old_file_name):
    old_file_path = Path(join(folder_path, old_file_name))
    metadata = get_metadata(get_file_handle(old_file_path, method=fitz))
    print('Metadata:\n', metadata)
    title = metadata['title']
    author = metadata['author']
    new_file_name = author + "-" + title + ".pdf"
    new_file_path = Path(join(folder_path, new_file_name))

    print('Rename "{old_file_name}" -> "{new_file_name}" in folder: "{folder_path}"'.format(old_file_name=old_file_name,
                                                                                            new_file_name=new_file_name,
                                                                                            folder_path=folder_path))
    # os.rename(old_file_path, new_file_path)


def parse_file(page, opt="text"):
    text = page.get_text(opt)
    return text


def test_file(path, method):
    '''
    methods:
           - "fitz" - PyMuPDF
           - "pdfplumber"  - pdfplumber
    :param path:
    :param method:
    :return:
    '''

    if method == pdfplumber:
        with method.open(path) as pdf:
            first_page = pdf.pages[0]
            print(first_page.extract_text())
            print(get_metadata(pdf))

    elif method == fitz:
        with method.open(path) as pdf:
            page = pdf.load_page(0)
            text = parse_file(page, "text")
            # print(text)
            print(get_metadata(pdf))


def check_metadata(folder_path, old_file_name):
    # read the Document
    doc: typing.Optional[Document] = None
    old_file_path = Path(join(folder_path, old_file_name))
    h = open(old_file_path, 'rb')
    doc = PDF.loads(h)

    # check whether we have read a Document
    assert doc is not None

    # print the ID using XMP meta info
    print("ID: %s" % doc.get_xmp_document_info().get_author())


def get_file():
    pdf_folder_path = Path(os.path.abspath("reward magnitude/reward expectancy (anticipation phase)"))
    print(pdf_folder_path)

    onlyfiles = [f for f in listdir(pdf_folder_path) if isfile(join(pdf_folder_path, f))]

    for file_name in onlyfiles:
        pdf_path = Path(join(pdf_folder_path, file_name))
        check_path(pdf_path)
        ##
        # rename_files(pdf_folder_path, file_name)
        check_metadata(pdf_folder_path, file_name)

def main():
    get_file()


if __name__ == '__main__':
    main()
