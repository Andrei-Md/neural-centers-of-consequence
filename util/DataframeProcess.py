import pandas as pd
import util.Data as data_util


def check_list(row, ch_list):
    for el in ch_list:
        if el in row: return True
    return False


def split_keys(row):
    str_set = set()
    for e in row:
        str_set.update(set(map(str.strip, e.split(';'))))
    return str_set


def df_process(df):
    # Focis Number
    df_result = df.groupby(['title', 'author']).size().reset_index(name="Number of Foci")

    ## Subjects number
    group_subjects = df.groupby(['title', 'author', 'subjects'])
    dict_keys_subjects = group_subjects.groups.keys()
    df_group_subjects = pd.DataFrame.from_records([*dict_keys_subjects],
                                                  columns=['title', 'author', 'Number of Subjects'])
    df_result = df_result.join(df_group_subjects[['title', 'Number of Subjects']].set_index('title'), on='title')

    ## Contrast
    df_group_contrast = df.groupby(['title', 'author'])['contrast'].apply(lambda x: set(x)).reset_index(
        name='contrast_set')
    df_result = df_result.join(df_group_contrast[['title', 'contrast_set']].set_index('title'), on='title')

    ## Keywords
    df_group_keywords = df.groupby(['title', 'author'])['keywords'].apply(lambda x: set(x)).reset_index(
        name='keywords_set')
    df_group_keywords['keywords_split'] = df_group_keywords['keywords_set'].apply(split_keys)
    df_result = df_result.join(df_group_keywords[['title', 'keywords_split']].set_index('title'), on='title')

    return df_result


def list_of_sets_to_set(df, column_name):
    list_of_set = list(df[column_name])
    set_all = set()
    for s in list_of_set:
        set_all.update(s)
    len(set_all)
    return set_all

def boolean_df(item_lists, unique_items):# Create empty dict
    bool_dict = {}

    # Loop through all the tags
    for i, item in enumerate(unique_items):

        # Apply boolean mask
        bool_dict[item] = item_lists.apply(lambda x: item in x)

    # Return the results as a dataframe
    return pd.DataFrame(bool_dict)

def df_report_process(df):
    #### Focis number wm
    df_group_focis = df.groupby(['title', 'author']
                                      ).size().reset_index(name="Number of Foci")

    #### Subjects number wm
    group_subjects = df.groupby(['title', 'author', 'subjects'])
    dict_keys_subjects = group_subjects.groups.keys()
    df_group_subjects = pd.DataFrame.from_records([*dict_keys_subjects],
                                                  columns=['title', 'author', 'Number of Subjects'])
    df_final = df_group_focis.join(df_group_subjects[['title', 'Number of Subjects']].set_index('title'), on='title')

    ## Get set of contrast
    df_group_contrast = df.groupby(['title', 'author'])['contrast'].apply(lambda x: set(x)).reset_index(
        name='contrast_set')
    df_final = df_final.join(df_group_contrast[['title', 'contrast_set']].set_index('title'), on='title')

    return df_final

def check_column_elem(df,colummn_name,check_set):
    '''
    the column to check must contains sets of elements
    :return: mask for the dataframe
    '''
    mask = df[colummn_name].apply(lambda x: check_list(x, check_set))
    return mask
