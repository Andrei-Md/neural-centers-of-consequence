import os
from os.path import join
from pathlib import Path
from FileProcess import FileProcess
import logging

from pdf import Util, Csv


def process_files():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    # logging.basicConfig(filename="main.log",
    #                     format='%(asctime)s %(message)s',
    #                     filemode='w')

    # all
    # pdf_folder_path = Path(os.path.abspath("all"))
    # pdf_folder_path = Path(os.path.abspath("pdfs/todo"))
    pdf_folder_path = Path(os.path.abspath("pdfs"))

    docs = FileProcess(path=pdf_folder_path, method="fitz", recursively=True)

    ## rename files
    # docs.rename_files(max_chars=40, ignore_files=["~"], ignore_folders=["~"])

    ## generate csv
    # docs.generate_csv(avoid=["-"], ignore_files=["~"], ignore_folders=["~"])

    # # # docs.create_xml("content.xml")
    df = docs.process_csv(n_lines=6, ignore_files=["gen_"], ignore_folders=["~"])

    # # # save df to csv
    csv_path = Path(join(os.path.abspath("../repr/data_db"), "final_coordinates-no_conversion.csv"))
    csv = Csv.Csv(csv_path, create=True)
    csv.create_csv_from_pd(df, header=True, index=False)

if __name__ == '__main__':
    process_files()
