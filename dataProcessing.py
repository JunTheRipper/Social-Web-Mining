# 数据预处理的模块
import pandas as pd
import collections
import os
import datetime
# deal with excel and etc.


def data_combine(filename:str):
    '''
    批量处理单个的excel格式文件
    :param filename: str
    :return df_data: pd.DataFrame
    '''
    df_ym = pd.read_excel(filename, sheet_name=None, index_col=None, na_values=['NA'])
    df_ym = collections.OrderedDict(sorted(df_ym.items()))
    df_data = pd.concat(df_ym.values(), ignore_index=True)
    return df_data


def data_renameweibo(df:pd.DataFrame) -> pd.DataFrame:
    '''
    实现相关列重命名,指微博数据，同时仅仅提取关键的内容、时间和信息
    :param df: 初始的pandas.DataFrame
    :return:
    '''
    return df.rename(columns={'微博内容':'content', '博主昵称':'author', '发布时间':'time'})



def multi_excel_combine(oslist:str) -> pd.DataFrame:
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


def multi_csv_combine(oslist:str) -> pd.DataFrame:
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


def multi_pd_combine(dx: pd.DataFrame, dy: pd.DataFrame) -> pd.DataFrame:
    '''
    两个pd.DataFrame格式的结合
    :param dx: pd.DataFrame
    :param dy: pd.DataFrame
    :return:
    '''
    df = pd.concat([dx, dy], ignore_index=True)
    return df


def show_nan_data(data: pd.DataFrame) -> None:
    '''
    查看是否处理了缺失值
    :param data: pd.DataFrame
    :return void
    '''
    print(data.isnull().sum())


def drop_nan_data(data: pd.DataFrame, key:str=None):
    '''
    数据去空值 —— for 丁香园等一般数据
    :param data: pd.DataFrame
    :return dropped_data: pd.DataFrame
    '''
    if key == None:
        dropped_data = data.dropna(axis=0, subset=["content"])
        dropped_data.reset_index(drop=True, inplace=True)
        # drop=True：删除原行索引；inplace=True:在数据上进行更新
        print("Data empty report: \n", dropped_data.isnull().any())
        return dropped_data

    else:
        dropped_data = data.dropna(axis=0, subset=[key])
        dropped_data.reset_index(drop=True, inplace=True)  # drop=True：删除原行索引；inplace=True:在数据上进行更新
        print("Data empty report: \n",dropped_data.isnull().any())
        return dropped_data


def drop_repeat_data(data: pd.DataFrame, key: str = None):
    '''
    数据去重复值 —— for 丁香园等其他模块
    :param key: str 关键词, content
    :param data: pd.DataFrame
    :return dropped_data: pd.DataFrame
    '''
    if key is None:
        # 爬微博数据
        unrepeated_data = data.drop_duplicates(['content'], keep='last')
        unrepeated_data.reset_index(drop=True, inplace=True)  # drop=True：删除原行索引；inplace=True:在数据上进行更新
        return unrepeated_data
    else:
        unrepeated_data = data.drop_duplicates([key], keep='last')
        unrepeated_data.reset_index(drop=True, inplace=True)  # drop=True：删除原行索引；inplace=True:在数据上进行更新
        return unrepeated_data


def drop_symbols(data: pd.DataFrame, key: str=None):
    '''
    数据去特殊值 —— 一般的未格式化的评论数据
    :param key: str 特定标注的关键词
    :param data: pd.DataFrame
    :return dropped_data: pd.DataFrame
    '''
    if key == None:
        data['content'] = data['content'].str.replace(r'[^\w]+', '')
        return data

    else:
        data[key] = data[key].str.replace(r'[^\w]+', '')
        return data

def show_head(data):
    '''

    :param data: pd.DataFrame
    :return:
    '''
    print(data.head())


def data_cut(data, lister=None) -> pd.DataFrame:
    """
    实现数据的截取，只截取微博用户名、用户内容、发布时间3列维度的数据
    :param lister: 获取数据截取的需要内容索引
    :param data:
    :return:
    """
    if lister is None:
        return data.loc[:,['author','content', 'time']]
    else:
        return data.loc[:,lister]


def time_composition(data:pd.DataFrame,
                     strTime: str = datetime.date.today().strftime("%Y-%m-%d")) \
        -> pd.DataFrame:
    '''
    社交媒体时间统一整合处理
    :param strTime:  输入当前日期，对日期数据处理(昨天、前天这类数据)
    :param data:  原始未处理的数据
    :return: data1 返回生成的列表数据
    说明这边的数据需要灵活处理
    '''
    data['time'] = data['time'].str.replace("年", "-").str.replace("月", "-")\
        .str.replace("日", "")

    datelist = []
    for date in data['time'].values:
        if date[2] == ":":
            # 只显示时间，是今天
            date = strTime
        if date[:2] == "昨天":
            oneday = datetime.timedelta(days=1)
            yes = datetime.date.today() - oneday
            date = yes.strftime("%Y-%m-%d")
        if date[:2] == "前天":
            oneday = datetime.timedelta(days=2)
            yes = datetime.date.today() - oneday
            date = yes.strftime("%Y-%m-%d")

        if date[:2] == "今天":
            date = strTime
        if not date[:2] == "20":
            date = "2021-" + date
        if date[-1] == "前":
            date = strTime
        datelist.append(date)

    data['time'] = datelist
    return data


def write_into_csv(data: pd.DataFrame, name: str, location: str = "results/random-nuclear/Res-Dat/"):
    """
    :param name: 存储csv文件名称
    :param data: pd.DataFrame
    :return: None
    """
    data.to_csv(location + name, index = False)
    print("CSV File Stored......")


def time_stamp(data: pd.DataFrame, sorted=False):
    '''
    时间级别数据格式整理和按照时间序列排序
    :param sorted:
    :param data:
    :return:
    '''
    data['time'] = pd.to_datetime(data['time'])
    if sorted == False:
        return data
    else:
        data.sort_values('time', inplace=True)
        return data



def deal_exception(data: pd.DataFrame):
    '''
    数据（以丁香园类数据为主）的异常处理技术
    :param data:
    :return:
    '''
    pass