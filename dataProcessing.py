# 数据预处理的模块
import pandas as pd
import collections
import os
# deal with excel and etc.


def data_combine(filename):
    '''
    批量处理单个的excel格式文件
    :param filename: str
    :return df_data: pd.DataFrame
    '''
    df_ym = pd.read_excel(filename, sheet_name=None, index_col=None, na_values=['NA'])
    df_ym = collections.OrderedDict(sorted(df_ym.items()))
    df_data = pd.concat(df_ym.values(), ignore_index=True)
    return df_data


def data_renameweibo(df) -> pd.DataFrame:
    '''
    实现相关列重命名,指微博数据，同时仅仅提取关键的内容、时间和信息
    :param df: 初始的pandas.DataFrame
    :return:
    '''
    return df.rename(columns={'微博内容':'content', '博主昵称':'author', '发布时间':'time'})





def multi_excel_combine(oslist):
    '''
    处理多个EXCEL数据，但是对于csv等格式需要另外处理
    :param oslist: list
    :return dfy: pd.DataFrame
    '''
    dfy = None
    for shortname in os.listdir(oslist):
        fullname = oslist + '/' + shortname
        dfx = data_combine(fullname)
        dfy = pd.concat([dfy, dfx], ignore_index=True)
    return dfy


def multi_csv_combine(oslist) -> pd.DataFrame:
    '''
    处理多个csv格式数据
    :param oslist:
    :return:
    '''
    dfy = None
    for shortname in os.listdir(oslist):
        fullname = oslist + '/' + shortname
        dfx = pd.read_csv(fullname)
        dfy = pd.concat([dfy, dfx], ignore_index=True)
    return dfy


def multi_pd_combine(dx, dy) -> pd.DataFrame:
    '''
    两个pd.DataFrame格式的结合
    :param dx: pd.DataFrame
    :param dy: pd.DataFrame
    :return:
    '''
    df = pd.concat([dx, dy], ignore_index=True)
    return df


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
    dropped_data = data.dropna(axis=0, subset=["content"])
    dropped_data.reset_index(drop=True, inplace=True)  # drop=True：删除原行索引；inplace=True:在数据上进行更新
    print("Data empty report: \n",dropped_data.isnull().any())
    return dropped_data


def drop_repeat_data(data):
    '''
    数据去重复值
    :param data: pd.DataFrame
    :return dropped_data: pd.DataFrame
    '''
    unrepeated_data = data.drop_duplicates(['content'], keep='last')
    unrepeated_data.reset_index(drop=True, inplace=True)  # drop=True：删除原行索引；inplace=True:在数据上进行更新
    return unrepeated_data


def drop_symbols(data):
    '''

    数据去特殊值
    :param data: pd.DataFrame
    :return dropped_data: pd.DataFrame
    '''
    data['content'] = data['content'].str.replace(r'[^\w]+', '')
    return data


def show_head(data):
    '''

    :param data: pd.DataFrame
    :return:
    '''
    print(data.head())

def data_cut(data):
    """
    实现数据的截取，只截取微博用户名、用户内容、发布时间3列维度的数据
    :param data:
    :return:
    """
    return data.loc[:,['author','content', 'time']]



def write_into_csv(data, name):
    """
    :param data: pd.DataFrame
    :return: None
    """
    data.to_csv("results/" + name)
    print("CSV File Stored......")

