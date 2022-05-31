import os
import threading
from pathlib import Path
import logging

import numpy as np
import pandas as pd
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString

from os import listdir
from os.path import isfile, join
import Pdf as Pdf
import traceback

from collections import OrderedDict

## borb
# import typing
# from borb.pdf.document.document import Document
# from borb.pdf.pdf import PDF
##
from pdf import Csv


def threadsafe_function(fn):
    """decorator making the decorated function thread safe"""
    lock = threading.Lock()

    def new(*args, **kwargs):
        lock.acquire()
        try:
            r = fn(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            lock.release()
        return r

    return new


class Pdfc():
    """
        methods:
           - "fitz" - PyMuPDF
           - "pdfplumber"  - pdfplumber
    """
    id = 0
    datas = {"subject", "title", "author", "keywords"}

    def __init__(self, path, method):
        self.path = path
        # self.files = self._get_files(path)
        self.method = method

    def _get_files(self, path, extension, start=None):
        if start:
            onlyfiles = [f for f in listdir(path) if
                         isfile(join(path, f)) and f.lower().endswith(extension) and not f.lower().startswith(
                             tuple(start))]
        else:
            onlyfiles = [f for f in listdir(path) if
                         isfile(join(path, f)) and f.lower().endswith(extension)]
        return onlyfiles

    def get_files_metadata(self, add_path=False, add_id=False):
        '''
        :return: dict of metadata
        '''
        meta_dict = {}

        # todo modify if want to go in subfolders
        pdf_files = self._get_files(self.path, 'pdf')
        for file_name in pdf_files:
            pdf_path = Path(join(self.path, file_name))
            try:
                pdf = Pdf.Pdf(pdf_path, self.method)
                # create dict
                metadata = pdf.get_metadata()
                pdf_dict = {key: metadata[key] for key in metadata.keys() & self.datas}

                # path relative to the self path
                if add_path:
                    pdf_dict['path'] = os.path.relpath(pdf_path.resolve(),
                                                       self.path)  # pdf_path.cwd() <- relative to cwd
                if add_id:
                    pdf_dict['id'] = self._get_id()

                meta_dict[pdf_path.name] = pdf_dict
            except Exception as e:
                # traceback.print_exc()
                message = "An exception of type {0} occurred: \t{1}\n\t\tOn File: {2}".format(type(e).__name__, e.args,
                                                                                              pdf_path.name)
                logging.error(message)
        return meta_dict

    def rename_files(self, ignore_files="", **kwargs):
        # todo modify if want to go in subfolders
        pdf_files = self._get_files(self.path, '.pdf', start=ignore_files)
        for file_name in pdf_files:
            pdf_path = Path(join(self.path, file_name))
            Pdf.check_path(pdf_path, extension='.pdf')
            self.rename_file(self.path, file_name, **kwargs)

    def rename_file(self, folder_path, old_file_name, max_chars=30):
        old_file_path = Path(join(folder_path, old_file_name))

        pdf = Pdf.Pdf(old_file_path, self.method)
        metadata = pdf.get_metadata()
        logging.info('Metadata:\n', metadata)

        title = (metadata["title"][:max_chars - 2] + '_') if len(metadata['title']) > max_chars else metadata["title"]
        author = metadata['author']
        importance = metadata['subject']

        new_file_name = importance + "_" + author + "_" + title + ".pdf"
        new_file_path = Path(join(folder_path, new_file_name))

        logging.info('Rename "{old_file_name}" -> "{new_file_name}" in folder: "{folder_path}"'.format(
            old_file_name=old_file_name,
            new_file_name=new_file_name,
            folder_path=folder_path))

        try:
            del pdf
            os.rename(old_file_path, new_file_path)
        except Exception:
            traceback.print_exc()
            logging.error(">> Cannot rename: " + "{old_file_name}".format(old_file_name=old_file_name))

    def generate_csv(self, ignore_files=["~"], **kwargs):
        # todo modify if want to go in subfolders
        pdf_files = self._get_files(self.path, '.pdf', start=ignore_files)
        for file_name in pdf_files:
            pdf_path = Path(join(self.path, file_name))
            Pdf.check_path(pdf_path, extension='.pdf')
            self.generate_csv_file(self.path, pdf_path, **kwargs)

    def generate_csv_file(self, folder_path, pdf_path, avoid, max_chars=30):
        pdf = Pdf.Pdf(pdf_path, self.method)
        metadata = pdf.get_metadata()
        if metadata["subject"] in avoid:
            return
        # create dict from pdf - since py 3.6 dict keep the order of insertion else use OrderedDict
        csv_dict = OrderedDict({"importance": metadata["subject"],
                                "author": metadata["author"],
                                "title": metadata["title"],
                                "table_name": "",
                                "contrast": "",
                                "keywords": metadata["keywords"]})
        df_csv = pd.DataFrame.from_dict(data=csv_dict, orient='index')

        importance = metadata["subject"]
        author = metadata["author"]
        title = (metadata["title"][:max_chars - 2] + '_') if len(metadata['title']) > max_chars else metadata["title"]
        # write pd to csv
        csv_file_name = "gen" + "_" + importance + "_" + author + "_" + title + ".csv"
        csv_path = Path(join(folder_path, csv_file_name))
        csv = Csv.Csv(csv_path, create=True)
        csv.create_csv_from_pd(df_csv, header=False)

    def create_xml(self, filename):
        # docs.rename_files()
        meta_dict = self.get_files_metadata(add_path=True, add_id=True)

        # add new lines to each item
        # update = {'table_path': ' '}
        # meta_list = [{**d, **update} for d in meta_list]
        # print to file
        xml = dicttoxml(meta_dict)  # , item_func=lambda x: 'list_item')
        xml = parseString(xml).toprettyxml(indent=' ' * 4)

        # print(xml)

        save_path_file = filename
        with open(Path(join(self.path, save_path_file, )), 'w') as f:
            f.write(xml)

    def process_csv(self, n_lines,ignore_files=""):
        files = self._get_files(self.path, 'csv', start=ignore_files)
        list = []
        for file_name in files:
            file_path = Path(join(self.path, file_name))
            try:
                csv = Csv.Csv(file_path)
                dict = csv.process_first_n_lines(n=n_lines)
                df = csv.create_pd_from_csv(skiprows=n_lines, converters={'Broadman Area': str})
                df = pd.concat([pd.DataFrame(dict, index=df.index), df], axis=1)
                list.append(df)
            except pd.errors.EmptyDataError as e:
                message = "An exception of type {0} occurred: \t{1}\n\t\tOn File: {2}".format(type(e).__name__, e.args,
                                                                                              file_path.name)
                logging.info(message)
            except Exception as e:
                # traceback.print_exc()
                message = "An exception of type {0} occurred: \t{1}\n\t\tOn File: {2}".format(type(e).__name__, e.args,
                                                                                              file_path.name)
                logging.error(message)
        result = pd.concat(list, ignore_index=True)
        return result

    @threadsafe_function
    def _incr_id(self):
        self.id += 1
        return self.id

    def _get_id(self):
        return self._incr_id()
