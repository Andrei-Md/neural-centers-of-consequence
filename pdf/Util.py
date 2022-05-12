import pandas as pd
# import supereeg as se
import visbrain.utils as vs
import numpy as np


def check_path(path, extension):
    if not path.exists() or path.suffix != extension:
        return False
    else:
        # print(path)
        return True


def transform_coordinate(df, keyword, columns_name, method):
    data_tmp = df[df['keywords'].str.contains(keyword)]

    # location columns to np
    np_coords = data_tmp.loc[:, data_tmp.columns.isin(columns_name)].to_numpy()
    # transform to desired coordinates
    mni_locs = np.round(method(np_coords).astype(float), decimals=3)
    # create new df wih the same indexes
    df_transf_coords = pd.DataFrame(mni_locs, columns=columns_name, index=data_tmp.index)

    # update old df
    df.update(df_transf_coords)
    # data_tmp['keywords'].replace(".*talairach;.*", "talairach(converted);", inplace=True, regex=True)
    df['keywords'].update(data_tmp['keywords'].apply(lambda x: x.replace(keyword + ";", keyword + "(converted);")))
    return df


def process_coordinates(data: pd.DataFrame, conversion_type, columns_name) -> pd.DataFrame:
    if conversion_type == 'tal2mni':
        return transform_coordinate(df=data, keyword='talairach', method=vs.tal2mni, columns_name=columns_name)
    elif conversion_type == 'min2tal':
        return transform_coordinate(df=data, keyword='MNI', method=vs.mni2tal, columns_name=columns_name)
    return data
