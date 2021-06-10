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

        self.X_pca = None
        self.X_pca_frame = None

    def lda_2(self):

        pass

    def lda_3(self):
        pass