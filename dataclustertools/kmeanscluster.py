import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import seaborn as sns
sns.set_style(style="darkgrid")

class KMeansController:
    def __init__(self, data: pd.DataFrame, PCA_data: pd.DataFrame):
        '''
        :param data: 原始数据
        :param PCA_data: pca降维后的数据
        '''
        self.data = data
        self.PCA_data = PCA_data

    def elbow_cluster_comment(self, savelocation = None, savename = None):
        '''
        聚类结果评价—— 肘部法
        :param savelocation:  图片存储路径
        :param savename:  图片存储文件名(前缀)
        :return: None 显示图片的情况
        '''
        plotlist = []
        for k in range(2, 10):
            est = KMeans(n_clusters=k, random_state=0).fit(self.PCA_data)
            plotlist.append(np.sqrt(est.inertia_))

        plt.plot(range(2, 10), plotlist, 'o-')
        plt.xlabel('k')

        if not savelocation is None:
            plt.savefig(savelocation + savename+'-elbow-KMEANS-cluster.png',
                        dpi=600)
        else:
            plt.show()

    def silhouette_cluster_comment(self, savelocation = None, savename = None):
        '''
        轮廓系数法评价聚类效果,轮廓系数可以用来选择合适的聚类数目。
        根据折线图可直观的找到系数变化幅度最大的点，
        认为发生畸变幅度最大的点就是最好的聚类数目。
        :param savelocation:  图片存储路径
        :param savename:  图片存储文件名(前缀)
        :return: None 显示图片的情况
        '''
        from sklearn.metrics import silhouette_score
        silscore = []
        for k in range(2, 10):
            est = KMeans(n_clusters=k, random_state=0).fit(self.PCA_data)
            silscore.append(silhouette_score(self.PCA_data, est.labels_))

        plt.plot(range(2, 10), silscore, 'o-')
        plt.xlabel('k')

        if not savelocation is None:
            plt.savefig(savelocation + savename+'-silhouette-KMEANS-cluster.png', dpi=600)
        else:
            plt.show()

    def calinski_Harabaz_comment(self):
        '''
        Calinski-Harabaz指数也可以用来选择最佳聚类数目，
        且运算速度远高于轮廓系数。
        当内部数据的协方差越小，类别之间的协方差越大，
        Calinski-Harabasz分数越高。
        :return: None
        '''
        from sklearn.metrics import calinski_harabasz_score
        for k in range(2, 10):
            est = KMeans(n_clusters=k, random_state=4).fit(self.PCA_data)
            score = calinski_harabasz_score(self.PCA_data, est.labels_)
            print('聚类%d簇的calinski_harabasz分数为：%f' % (k, score))


    def cluster_KMeans(self, number: int) -> pd.DataFrame:
        '''
        KMeans聚类
        :param number:  聚类数目
        :return: 聚类后的标签添加情况
        '''
        from sklearn.cluster import KMeans
        # 此处指定K=12
        est = KMeans(n_clusters=number)
        est.fit(self.PCA_data)
        # 获取数据标签值
        kmeans_clustering_labels = pd.DataFrame(est.labels_, columns=['cluster'])
        # 将聚类结果与降维特征数据进行拼接
        self.PCA_data = pd.concat([self.PCA_data, kmeans_clustering_labels], axis=1)
        # print(self.X_pca_frame)
        t = self.data
        t = pd.concat([t, kmeans_clustering_labels], axis=1)
        return t

    def show_scatter_result(self, dimension: int = 3, savelocation = None, savename = None):
        '''
        散点图显示大致的聚类情况
        :param dimension: 维度，默认为3 表示散点图是3D的，反正2 2D
        :return: 散点图
        '''
        if dimension == 3:
            from mpl_toolkits.mplot3d import Axes3D
            cluster_1_color = {0: 'red', 1: 'green', 2: 'blue', 3: 'yellow', 4: 'cyan', 5: 'black', 6: 'magenta',
                               7: '#fff0f5', 8: '#ffdab9', 9: '#ffa500'}
            colors_clustered_data = self.PCA_data['cluster'].map(cluster_1_color)
            fig_clustered_data = plt.figure()
            ax_clustered_data = fig_clustered_data.add_subplot(111, projection='3d')
            ax_clustered_data.scatter(self.PCA_data['pca_1'].values, self.PCA_data['pca_2'].values,
                                      self.PCA_data['pca_3'].values, c=colors_clustered_data)
            ax_clustered_data.set_xlabel('Component 1')
            ax_clustered_data.set_ylabel('Component 2')
            ax_clustered_data.set_zlabel('Component 3')

            if not savelocation is None:
                plt.savefig(savelocation + savename + '-silhouette-KMEANS-cluster.png', dpi=600)
            else:
                plt.show()

        else:
            pass

    def show_data(self) -> pd.DataFrame:
        '''

        :return: 显示当前的data情况（可能做了聚类，拿出来看看）
        '''
        return self.data