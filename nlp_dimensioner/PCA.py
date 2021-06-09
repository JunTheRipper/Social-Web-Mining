
import pandas as pd
import jieba
from sklearn.decomposition import PCA


class PCAController:
    def __init__(self, data: pd.DataFrame, countvector: pd.DataFrame) -> None:
        '''
        :param data: 社交评论自然语言原始数据
        :param countvector: 社交评论自然语言以处理的词频矩阵
        '''
        self.data = data
        self.countvector = countvector

        self.X_pca = None
        self.X_pca_frame = None

    def pca_2(self):
        '''

        :return: 降维2维
        '''
        # 此处的主成分维度我们人为设定为2，对于属性较少的数据集，属于常规会选择的维度数，后面也会看到，这个也是出于可以可视化的需求
        pca = PCA(n_components=2)
        # 将设置了维数的模型作用到标准化后的数据集并输出查看
        self.X_pca = pca.fit_transform(self.countvector)
        self.X_pca_frame = pd.DataFrame(self.X_pca, columns=['pca_x', 'pca_y'])
        # print(self.X_pca_frame)
        return self.X_pca_frame


    def pca_3(self) -> pd.DataFrame:
        # 此处的主成分维度我们人为设定为3，对于属性较少的数据集，属于常规会选择的维度数，后面也会看到，这个也是出于可以可视化的需求
        new_pca = PCA(n_components=3)
        # 将设置了维数的模型作用到标准化后的数据集并输出查看
        self.X_pca = new_pca.fit_transform(self.countvector)
        self.X_pca_frame = pd.DataFrame(self.X_pca, columns=['pca_1', 'pca_2', 'pca_3'])
        # print(self.X_pca_frame)
        return self.X_pca_frame

    def cluster_KMeans(self, number) -> pd.DataFrame:
        '''KMeans聚类'''
        from sklearn.cluster import KMeans

        est = KMeans(n_clusters=number)
        est.fit(self.X_pca)
        # 获取数据标签值
        kmeans_clustering_labels = pd.DataFrame(est.labels_, columns=['cluster'])
        # 将聚类结果与降维特征数据进行拼接
        self.X_pca_frame = pd.concat([self.X_pca_frame, kmeans_clustering_labels], axis=1)
        # print(self.X_pca_frame)
        return self.X_pca_frame

