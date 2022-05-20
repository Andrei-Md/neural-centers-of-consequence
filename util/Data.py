import numpy as np
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


def mni2tal(data):
    '''
    Convert the coordinates from MNI coordinate space into Talairach coordinate space.
    Based on paper:
     Lancaster et al - Bias Between MNI and Talairach Coordinates Analyzed Using the ICBM-152 Brain Template
    :param data: numpy data (,3) to be converted
    :return: converted data (,3)
    '''

    # check shape
    if not data.shape[1] == 3:
        raise TypeError("data shape should be (n,3), n>=1");

    mtt = np.array(
        [
            [0.9357, 0.0029, -0.0072, -1.0423],
            [-0.0065, 0.9396, -0.0726, -1.3940],
            [0.0103, 0.0752, 0.8967, 3.6475],
            [0.0, 0.0, 0.0, 1.0]
        ]
    )

    data = np.c_[data, np.ones(data.shape[0])]

    # np.apply_along_axis(np.dot(mtt), axis=1, arr=data)
    data = np.array([np.dot(mtt,row) for row in data])
    return data[:,:3]

def tal2mni(data):
    '''
    Convert the coordinates from Talairach coordinate space into MNI coordinate space. MTT^(-1) * r
    Based on paper:
     Lancaster et al - Bias Between MNI and Talairach Coordinates Analyzed Using the ICBM-152 Brain Template
    :param data: numpy data (,3) to be converted
    :return: converted data (,3)
    '''
    # check shape
    if not data.shape[1] == 3:
        raise TypeError("data shape should be (n,3), n>=1");

    mtt = np.linalg.inv(np.array(
        [
            [0.9357, 0.0029, -0.0072, -1.0423],
            [-0.0065, 0.9396, -0.0726, -1.3940],
            [0.0103, 0.0752, 0.8967, 3.6475],
            [0.0, 0.0, 0.0, 1.0]
        ]
    ))

    data = np.c_[data, np.ones(data.shape[0])]

    # np.apply_along_axis(np.dot(mtt), axis=1, arr=data)
    data = np.array([np.dot(mtt,row) for row in data])
    return data[:,:3]