# 丁香园类数据特征工程文件
import pandas as pd

class Feature:
    def __init__(self, data):
        self.data = data
        self.transformed_data = None  # 做了相关处理，无量纲化的数据集
    def std(self):
        '''
        无量纲化
        标准化：标准化的前提是特征值服从正态分布，标准化后，其转换成标准正态分布。
        最大最小归一化：最小值-最大值归一化是将训练集中原始数据中特征的取值缩放到0到1之间。这种特征缩放方法实现对原始数据的等比例缩放，比较适用于数值比较集中的情况。
        :return: std_data
        '''
        from sklearn.preprocessing import StandardScaler
        sc_X = StandardScaler(copy=True)
        std_data = pd.DataFrame(sc_X.fit_transform(self.data))
        return std_data

    def vts(self):
        '''
        方差选择法：首先我们用方差选择方作为特征选择的预处理。
        :return:
        '''
        from sklearn.feature_selection import SelectKBest
        from sklearn.feature_selection import chi2
        from sklearn.feature_selection import VarianceThreshold
        data_after_var = VarianceThreshold(threshold=0.01).fit_transform(self.data)  # 使用阈值0.01进行选择
        return data_after_var

