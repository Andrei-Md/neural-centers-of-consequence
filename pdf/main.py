import os
from os.path import join
from pathlib import Path
from Pdfc import Pdfc
import logging

from pdf import Util, Csv


def main():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    # logging.basicConfig(filename='main.log', level=logging.DEBUG)

    # pdf_folder_path = Path(
    #     os.path.abspath("reward magnitude/assessed processing of reward receipt (outcome phase)/in-work"))
    # pdf_folder_path = Path(
    #     os.path.abspath("reward magnitude/assessed processing of reward receipt (outcome phase)"))
    # pdf_folder_path = Path(
    #     os.path.abspath("reward magnitude/reward expectancy (anticipation phase)"))
    pdf_folder_path = Path(
        os.path.abspath("all"))
    docs = Pdfc(pdf_folder_path, method="fitz")

    ## rename files
    # docs.rename_files(max_chars=40, ignore_files=["~"])

    ## generate csv
    # docs.generate_csv(avoid=["-"], ignore_files=["~"])

    # # # docs.create_xml("content.xml")
    df = docs.process_csv(ignore_files=["gen_"])
    #
    # # ## process data
    # df = Util.process_coordinates(df, conversion_type='tal2mni', columns_name=['X(R)', 'Y(A)', 'Z(S)'])
    df = Util.process_coordinates(df, conversion_type='none', columns_name=['X(R)', 'Y(A)', 'Z(S)'])
    #
    # # # save df to csv
    csv_path = Path(join(os.path.abspath("reward magnitude"), "final_coordinates-no_conversion.csv"))
    csv = Csv.Csv(csv_path, create=True)
    csv.create_csv_from_pd(df, header=True, index=False)


if __name__ == '__main__':
    main()
