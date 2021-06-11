# 社交媒体情感挖掘模块
from snownlp import SnowNLP
import pandas as pd
import numpy as np


class DataEmotioner:
    def __init__(self, data):
        self.data = data # data -> pd.DataFrame
        self.score = []
        self.emaverage = None

    def emotion(self):

        for item in self.data['content']:
            s = SnowNLP(item)
            self.score.append(s.sentiments)
        self.data.loc[:, 'emotion_score'] = self.score
        self.emaverage = self.data['emotion_score'].to_frame().describe()
        return self.data

    def store(self, name):
        self.data.to_csv(name)


if __name__ == "__main__":
    file = pd.read_csv('results/allRightRandom.csv')

    em = DataEmotioner(file)
    em.emotion()
    em.store('results/random-right/emotion_label.csv')
    print(em.emaverage)