import pandas as pd


def import_data(csv_filename):
    data_df = pd.read_csv(csv_filename)
    # convert Broadman Area column values to string
    data_df['Broadman Area'] = data_df['Broadman Area'].astype(str)
    # data_df['BA_no'] = data_df['BA_no'].astype(str)
    # Convert Name column to lower string
    data_df["Name"] = data_df["Name"].str.lower()
    # add index column
    data_df['index_col'] = data_df.index
    return data_df
