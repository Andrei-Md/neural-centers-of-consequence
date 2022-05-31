import numpy as np
import pandas as pd


def import_data(csv_filename):
    data_df = pd.read_csv(csv_filename)

    # convert columns column values to string
    list_col_string= ['importance', 'author', 'title', 'table_name', 'contrast', 'keywords', 'Name',
                                   'Left/Right', 'Broadman Area']
    for col_name in list_col_string:
        data_df[col_name] = data_df[col_name].astype('string')

    # Convert columns to lower string
    list_col_to_lower = ['Name', "contrast", "Left/Right"]
    for col_name in list_col_to_lower:
        data_df[col_name] = data_df[col_name].str.lower()

    # remove leading/trail spaces from string columns

    list_col_remove_whitespaces = list_col_string
    for col_name in list_col_remove_whitespaces:
        data_df[col_name] = data_df[col_name].str.strip()

    # add index column
    data_df['index_col'] = data_df.index
    return data_df


def mni2tal(data):
    '''
    Convert the coordinates from MNI coordinate space into Talairach coordinate space.
    Based on paper:
     Lancaster et al - Bias Between MNI and Talairach Coordinates Analyzed Using the ICBM-152 Brain Template
    :param data: numpy data_db (,3) to be converted
    :return: converted data_db (,3)
    '''

    # check shape
    if not data.shape[1] == 3:
        raise TypeError("data_db shape should be (n,3), n>=1");

    mtt = np.array(
        [
            [0.9357, 0.0029, -0.0072, -1.0423],
            [-0.0065, 0.9396, -0.0726, -1.3940],
            [0.0103, 0.0752, 0.8967, 3.6475],
            [0.0, 0.0, 0.0, 1.0]
        ]
    )

    data = np.c_[data, np.ones(data.shape[0])]

    # np.apply_along_axis(np.dot(mtt), axis=1, arr=data_db)
    data = np.array([np.dot(mtt, row) for row in data])
    return data[:, :3]


def tal2mni(data):
    '''
    Convert the coordinates from Talairach coordinate space into MNI coordinate space. MTT^(-1) * r
    Based on paper:
     Lancaster et al - Bias Between MNI and Talairach Coordinates Analyzed Using the ICBM-152 Brain Template
    :param data: numpy data_db (,3) to be converted
    :return: converted data_db (,3)
    '''
    # check shape
    if not data.shape[1] == 3:
        raise TypeError("data_db shape should be (n,3), n>=1");

    mtt = np.linalg.inv(np.array(
        [
            [0.9357, 0.0029, -0.0072, -1.0423],
            [-0.0065, 0.9396, -0.0726, -1.3940],
            [0.0103, 0.0752, 0.8967, 3.6475],
            [0.0, 0.0, 0.0, 1.0]
        ]
    ))

    data = np.c_[data, np.ones(data.shape[0])]

    # np.apply_along_axis(np.dot(mtt), axis=1, arr=data_db)
    data = np.array([np.dot(mtt, row) for row in data])
    return data[:, :3]


def df_counter(df, column, set_keywords=None, default_nan_val=None, order=1):
    df_tmp = df.copy()
    count_elem = {}
    count_nans = {}
    # check nan
    if default_nan_val is None:
        mask_nan = df_tmp[column].isna()
    else:
        mask_nan = (df_tmp[column] == default_nan_val)
    count_nans['>nan_values<'] = df_tmp[mask_nan].shape[0]
    df_tmp = df_tmp[~mask_nan]

    # create set of keywords
    if set_keywords is None:
        set_keywords = df_tmp[column].unique()
    # print(set_keywords)

    for val in set_keywords:
        count_elem[val] = df_tmp[column][df_tmp[column] == val].count()
    count_elem = {k: v for k, v in sorted(count_elem.items(), key=lambda item: item[order])}

    count_nans.update(count_elem)
    return count_nans
