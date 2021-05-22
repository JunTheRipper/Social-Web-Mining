# 数据预处理的模块
import pandas as pd
import collections
import os
# deal with excel and etc.


def data_combine(filename):
    '''

    :param filename: str
    :return df_data: pd.DataFrame
    '''
    df_ym = pd.read_excel(filename, sheet_name=None, index_col=None, na_values=['NA'])
    df_ym = collections.OrderedDict(sorted(df_ym.items()))
    df_data = pd.concat(df_ym.values(), ignore_index=True)
    return df_data


def multi_excel_combine(oslist):
    '''

    :param oslist: list
    :return dfy: pd.DataFrame
    '''
    dfy = None
    for shortname in os.listdir(oslist):
        fullname = oslist + '/' + shortname
        dfx = data_combine(fullname)
        dfy = pd.concat([dfy, dfx], ignore_index=True)
    return dfy


def show_nan_data(data):
    '''
    查看是否处理了缺失值
    :param data: pd.DataFrame
    :return void
    '''
    print(data.isnull().sum())


def drop_nan_data(data):
    '''
    数据去空值
    :param data: pd.DataFrame
    :return dropped_data: pd.DataFrame
    '''
    dropped_data = data.dropna(axis=0, subset=["微博内容"])
    dropped_data.reset_index(drop=True, inplace=True)  # drop=True：删除原行索引；inplace=True:在数据上进行更新
    print("Data empty report: \n",dropped_data.isnull().any())
    return dropped_data


def drop_repeat_data(data):
    '''
    数据去重复值
    :param data: pd.DataFrame
    :return dropped_data: pd.DataFrame
    '''
    unrepeated_data = data.drop_duplicates(['微博内容'], keep='last')
    unrepeated_data.reset_index(drop=True, inplace=True)  # drop=True：删除原行索引；inplace=True:在数据上进行更新
    return unrepeated_data


def drop_symbols(data):
    '''

    数据去特殊值
    :param data: pd.DataFrame
    :return dropped_data: pd.DataFrame
    '''
    data['微博内容'] = data['微博内容'].str.replace(r'[^\w]+', '')
    return data


def show_head(data):
    '''

    :param data: pd.DataFrame
    :return:
    '''
    print(data.head())

def data_cut_weibo(data):
    """
    实现数据的截取，只截取微博用户名、用户内容、发布时间3列维度的数据
    :param data:
    :return:
    """
    return data.loc[:,['博主昵称','微博内容', '发布时间']]


def write_into_csv(data, name):
    """
    :param data: pd.DataFrame
    :return: None
    """
    data.to_csv("results/" + name)
    print("CSV File Stored......")

