# DBSCAN 基于密度聚类算法模块
import pandas as pd


class DBSCANController:
    def __init__(self, data: pd.DataFrame, PCA_data: pd.DataFrame):
        '''
        :param data: 原始数据
        :param PCA_data: pca降维后的数据
        '''
        self.data = data
        self.PCA_data = PCA_data