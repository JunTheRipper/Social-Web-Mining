from sklearn.cluster import KMeans
#加载绘图模块
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
import seaborn as sns
sns.set_style(style="darkgrid")
import jieba
import pandas as pd
import numpy as np
# 社交媒体主题聚类模块，可选使用： KMeans/AP/DBSCAN

def tokenizer(sentense):
    words = []
    cut = jieba.cut(sentense)
    for word in cut:
        words.append(word)
    return words


class DataCluster:
    def __init__(self, data, key):
        self.data = data # 注意：这里是用jieba处理过的词汇dataContent.csv
        self.stopwords = [] #去停用词列表
        for stopword in open('stopwords/baidu_stopwords.txt', 'r', encoding='utf-8'):
            self.stopwords.append(stopword.strip())
        self.countvector = None
        self.key = key

    def generate_wordcountvector(self) -> np.ndarray:
        count = CountVectorizer(tokenizer=tokenizer, stop_words=list(self.stopwords))
        countvector = count.fit_transform(self.data['dataContent']).toarray()
        # print(countvector)
        self.countvector = countvector
        return countvector

    def pca_2(self) -> pd.DataFrame:
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
        # 此处指定K=12
        est = KMeans(n_clusters=number)
        est.fit(self.X_pca)
        # 获取数据标签值
        kmeans_clustering_labels = pd.DataFrame(est.labels_, columns=['cluster'])
        # 将聚类结果与降维特征数据进行拼接
        self.X_pca_frame = pd.concat([self.X_pca_frame, kmeans_clustering_labels], axis=1)
        # print(self.X_pca_frame)
        return self.X_pca_frame

    def cluster_comment(self):
        '''聚类结果评价'''
        plotlist = []
        for k in range(2, 10):
            est = KMeans(n_clusters=k, random_state=0).fit(self.X_pca)
            plotlist.append(np.sqrt(est.inertia_))

        plt.plot(range(2, 10), plotlist, 'o-')
        plt.xlabel('k')
        plt.savefig(self.key+'-cluster.png',dpi=600)

        from sklearn.metrics import silhouette_score
        silscore = []
        for k in range(2, 10):
            est = KMeans(n_clusters=k, random_state=0).fit(self.X_pca)
            silscore.append(silhouette_score(self.X_pca, est.labels_))

        plt.plot(range(2, 10), plotlist, 'o-')
        plt.xlabel('k')
        plt.show()

    def show_cluster_result(self):

        pass


if __name__ == '__main__':
    data = pd.read_csv("results/random-right/dataContent.csv")
    print(data.head())
    dataCluster = DataCluster(data, "right")
    print(dataCluster.generate_wordcountvector())
    dt =dataCluster.pca_3()
    # dataCluster.cluster_comment()

    # 绘图
    from mpl_toolkits.mplot3d import Axes3D

    cluster_1_color = {0: 'red', 1: 'green', 2: 'blue', 3: 'yellow', 4: 'cyan', 5: 'black', 6: 'magenta', 7: '#fff0f5',
                       8: '#ffdab9', 9: '#ffa500'}
    colors_clustered_data = dt['cluster'].map(cluster_1_color)
    fig_clustered_data = plt.figure()
    ax_clustered_data = fig_clustered_data.add_subplot(111, projection='3d')
    ax_clustered_data.scatter(dt['pca_1'].values, dt['pca_2'].values, dt['pca_3'].values,
                              c=colors_clustered_data)
    ax_clustered_data.set_xlabel('Component 1')
    ax_clustered_data.set_ylabel('Component 2')
    ax_clustered_data.set_zlabel('Component 3')