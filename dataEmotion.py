# 社交媒体情感挖掘模块
from snownlp import SnowNLP
import pandas as pd
import numpy as np


class DataEmotioner:
    def __init__(self, data):
        self.data = data # data -> pd.DataFrame
        self.score = []

    def emotion(self):

        for item in self.data['微博内容']:
            s = SnowNLP(item)
            self.score.append(s.sentiments)
        self.data.loc[:, 'emotion_score'] = self.score

        return self.data

    def store(self, name):
        self.data.to_csv(name)

    def emaverage(self):
        '''显示相关信息'''
        return self.data['emotion_score'].to_frame().describe()

if __name__ == "__main__":
    file = pd.read_csv('results/allRightRandom.csv')

    em = DataEmotioner(file)
    em.emotion()
    em.store('results/random-right/emotion_label.csv')
    print(em.emaverage())