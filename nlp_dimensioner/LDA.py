import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis  #LDA


class LDAController:
    def __init__(self, data: pd.DataFrame, countvector: pd.DataFrame) -> None:
        '''
        :param data: 社交评论自然语言原始数据
        :param countvector: 社交评论自然语言以处理的词频矩阵
        '''
        self.data = data
        self.countvector = countvector

        self.X_lda = None
        self.X_lda_frame = None

    def lda_2(self):
        lda = LinearDiscriminantAnalysis(n_components=2)
        # 将设置了维数的模型作用到标准化后的数据集并输出查看
        self.X_lda = lda.fit_transform(self.countvector)
        self.X_lda_frame = pd.DataFrame(self.X_lda, columns=['lda_1', 'lda_2'])
        # print(self.X_pca_frame)
        return self.X_lda_frame

    def lda_3(self):
        lda = LinearDiscriminantAnalysis(n_components=3)
        # 将设置了维数的模型作用到标准化后的数据集并输出查看
        self.X_lda = lda.fit_transform(self.countvector)
        self.X_lda_frame = pd.DataFrame(self.X_lda, columns=['lda_1', 'lda_2','lda_3'])
        # print(self.X_pca_frame)
        return self.X_lda_frame

    def lda_n(self, n: int):
        col = []
        for i in range(n):
            col.append("lda_" + str(i + 1))
        # 此处的主成分维度我们人为设定为n，对于属性较少的数据集，属于常规会选择的维度数，后面也会看到，这个也是出于可以可视化的需求
        lda = LinearDiscriminantAnalysis(n_components=n)
        # 将设置了维数的模型作用到标准化后的数据集并输出查看
        self.X_lda = lda.fit_transform(self.countvector)
        self.X_lda_frame = pd.DataFrame(self.X_lda, columns=col)

        return self.X_lda_frame