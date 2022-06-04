import json
import os

import pandas as pd
import util.Data as data_util


def check_list(row, ch_list):
    for el in ch_list:
        if type(row) == str:
            if row == el:
                return True
        elif el in row:
            return True
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


def df_process2(df):
    # Focis Number
    df_result = df.groupby(['title', 'author', 'table_name']).size().reset_index(name="Number of Foci")

    ## Subjects number
    group_subjects = df.groupby(['title', 'author', 'table_name', 'subjects'])
    dict_keys_subjects = group_subjects.groups.keys()
    df_group_subjects = pd.DataFrame.from_records([*dict_keys_subjects],
                                                  columns=['title', 'author', 'table_name', 'Number of Subjects'])
    # df_result = df_result.join(df_group_subjects[['table_name', 'Number of Subjects']].set_index('table_name'),
    #                            on='table_name')
    df_result = pd.merge(left=df_result, right=df_group_subjects[['title', 'author', 'table_name', 'Number of Subjects']],
                         how='left', left_on=['title', 'author', 'table_name'],
                         right_on=['title', 'author', 'table_name'])

    ## Contrast
    df_group_contrast = df.groupby(['title', 'author', 'table_name'])['contrast'].apply(lambda x: set(x)).reset_index(
        name='contrast_set')
    df_result = pd.merge(left=df_result, right=df_group_contrast[['title', 'author', 'table_name', 'contrast_set']],
                         how='left', left_on=['title', 'author', 'table_name'],
                         right_on=['title', 'author', 'table_name'])
    ## Keywords
    df_group_keywords = df.groupby(['title', 'author', 'table_name'])['keywords'].apply(lambda x: set(x)).reset_index(
        name='keywords_set')
    df_group_keywords['keywords_split'] = df_group_keywords['keywords_set'].apply(split_keys)
    df_result = pd.merge(left=df_result, right=df_group_keywords[['title', 'author', 'table_name', 'keywords_split']],
                         how='left', left_on=['title', 'author', 'table_name'],
                         right_on=['title', 'author', 'table_name'])
    return df_result


def list_of_sets_to_set(df, column_name):
    list_of_set = list(df[column_name])
    set_all = set()
    for s in list_of_set:
        set_all.update(s)
    len(set_all)
    return set_all


def boolean_df(item_lists, unique_items):  # Create empty dict
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


def check_column_elem(df, colummn_name, check_set):
    '''
    the column to check must contains sets of elements
    :return: mask for the dataframe
    '''
    if len(check_set) == 0:
        return df[colummn_name].apply(lambda x: True)
    else:
        return df[colummn_name].apply(lambda x: check_list(x, check_set))


def check_splits(df, contrast_col_name='contrast_split', keyword_col_name='keywords_split', order=1):
    list_contrast_reward = list(list_of_sets_to_set(df, contrast_col_name))
    counter_contrast_reward = data_util.df_counter(df=df.explode(contrast_col_name), column=contrast_col_name,
                                                   set_keywords=list_contrast_reward, order=order)
    print("Contrast Splits:")
    print(json.dumps(counter_contrast_reward, indent=2, default=str))

    # %%
    list_keywords_reward = list(list_of_sets_to_set(df, keyword_col_name))
    counter_keywords_reward = data_util.df_counter(df=df.explode(keyword_col_name), column=keyword_col_name,
                                                   set_keywords=list_keywords_reward, order=order)
    print("Keywords Splits:")
    print(json.dumps(counter_keywords_reward, indent=2, default=str))


def get_elem_by_substring(df, column_name, lst_substr) -> set:
    set_keywords = set()
    for key in lst_substr:
        set_keywords.update(
            [el for el in list_of_sets_to_set(df, column_name) if el.find(key) != -1])
    return set_keywords


def dataframe_to_sleuth_txt(df, file_path, file_name, title_max_chars=40):
    file = os.path.join(os.path.abspath(file_path), file_name)
    # %%
    # sort data by author
    df_wm_select1 = df.sort_values(by=['title'])
    df_wm_select1.columns.values.tolist()
    # %%
    title = ''
    with open(file, 'w') as f:
        f.write('// Reference=MNI\n')
        for index, row in df_wm_select1.iterrows():
            if row['title'] != title:  # new title write the report metadata
                title = row['title']
                f.write('// {author}:{title}\n'.format(author=row['author'],
                                                       title=(row['title'][:title_max_chars] + '..') if
                                                       len(row['title']) > title_max_chars else row['title']))
                f.write('// Subjects={subjects}\n'.format(subjects=row['subjects']))
            f.write('{mnix} {mniy} {mniz}\n'.format(mnix=row['MNIX'], mniy=row['MNIY'], mniz=row['MNIZ']))
