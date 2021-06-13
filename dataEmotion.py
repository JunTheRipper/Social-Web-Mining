# 社交媒体情感挖掘模块
from snownlp import SnowNLP
import pandas as pd
import numpy as np
import re
import jieba.posseg as psg
import matplotlib.pyplot as plt
from wordcloud import WordCloud

class DataEmotioner:
    def __init__(self, data):
        self.data = data # data -> pd.DataFrame
        self.score = []
        self.emaverage = None
        self.seg_word = None
        self.data_res = None

    def easysnow_emotion(self):

        for item in self.data['content']:
            s = SnowNLP(item)
            self.score.append(s.sentiments)
        self.data.loc[:, 'emotion_score'] = self.score
        self.emaverage = self.data['emotion_score'].to_frame().describe()
        return self.data

    def store(self, name):
        self.data.to_csv(name, index=False)

    def target_data(self):
        '''
        词性标注
        :return:
        '''
        weibodata3 = self.data
        weibodata4 = weibodata3.copy()
        weibodata4[["content"]].drop_duplicates()
        content = weibodata3["content"]
        str_info = re.compile('[0-9a-zA-Z]')
        content = content.apply(lambda x: str_info.sub('', x))

        worker = lambda s: [(x.word, x.flag) for x in psg.cut(s)]
        self.seg_word = content.apply(worker)
        return self.seg_word

    def data_split_word(self):
        n_word = self.seg_word.apply(lambda x: len(x))

        n_content = [[x + 1] * y for x, y in zip(list(self.seg_word.index), list(n_word))]
        index_content = sum(n_content, [])

        seg_word = sum(self.seg_word, [])

        word = [x[0] for x in seg_word]
        nature = [x[1] for x in seg_word]

        result = pd.DataFrame({
            "index_content": index_content,
            "word": word,
            "nature": nature
        })

        result = result[result['nature'] != 'x']
        # 停用词读取
        stop_path = open("stopwords/cn_stopwords.txt", "r", encoding='UTF-8')
        stop = stop_path.readlines()
        stop = [i.replace('\n', '') for i in stop]
        # 去停用词
        word_list = list(set(word) - set(stop))
        result = result[result['word'].isin(word_list)]
        self.data_res = result

    def dic_combine(self, font_name:str, pic_name:str,
                        write_cloud_name:str):
        '''
        词典合并+词云图技术
        :param font_name:  字体路径
        :param pic_name:  图片路径
        :param write_cloud_name:  词云图生成路径
        :return: None
        '''
        list(self.data_res.groupby(by=['index_content']))
        # 计算每条评论的词数
        n_word = list(self.data_res.groupby(by=['index_content'])['index_content'].count())
        # 词数展开
        index_word = [list(np.arange(0, y)) for y in n_word]
        # 新建词数序号列
        index_word = sum(index_word, [])
        self.data_res['index_word'] = index_word
        # 去除全是名词的评论
        ind = self.data_res[['n' in x for x in self.data_res['nature']]]['index_content'].unique()
        result = self.data_res[[x in ind for x in self.data_res['index_content']]]
        # 读取词典并合并评价与感情词语，为正面赋值1，负面赋值-1
        pos_comment = open("正面评价词语（中文）.txt", "r", encoding='ANSI')
        pos_comment = pos_comment.readlines()
        pos_comment = [i.replace('\n', '') for i in pos_comment]
        pos_comment = [i.replace(' ', '') for i in pos_comment]
        pos_comment = pd.DataFrame(pos_comment)
        neg_comment = open("负面评价词语（中文）.txt", "r", encoding='ANSI')
        neg_comment = neg_comment.readlines()
        neg_comment = [i.replace('\n', '') for i in neg_comment]
        neg_comment = [i.replace(' ', '') for i in neg_comment]
        neg_comment = pd.DataFrame(neg_comment)
        pos_emotion = open("正面情感词语（中文）.txt", "r", encoding='ANSI')
        pos_emotion = pos_emotion.readlines()
        pos_emotion = [i.replace('\n', '') for i in pos_emotion]
        pos_emotion = [i.replace(' ', '') for i in pos_emotion]
        pos_emotion = pd.DataFrame(pos_emotion)
        neg_emotion = open("负面情感词语（中文）.txt", "r", encoding='ANSI')
        neg_emotion = neg_emotion.readlines()
        neg_emotion = [i.replace('\n', '') for i in neg_emotion]
        neg_emotion = [i.replace(' ', '') for i in neg_emotion]
        neg_emotion = pd.DataFrame(neg_emotion)
        positive = pos_comment.append(pos_emotion)
        negative = neg_comment.append(neg_emotion)
        positive["weight"] = [1] * len(positive)
        negative["weight"] = [-1] * len(negative)
        posneg = positive.append(negative)
        posneg.columns = ['word', 'weight']

        test = list(result["word"])
        test2 = list(posneg["word"])
        # 以word将词典对应值加到test3列表
        test3 = list()
        k = 1
        for i in range(0, len(result)):
            for j in range(0, len(posneg)):
                if test[i] == test2[j]:
                    k = 0
                    if j < 4565:
                        test3.append(1)
                        break
                    else:
                        test3.append(-1)
                        break
                k = 1
            if k == 1:
                test3.append(np.NaN)
        # 将test3合并到result
        test3 = pd.DataFrame(test3)
        result = result.reset_index(drop=False)
        result['weight'] = test3

        onlyresult = result.dropna()
        # 以评论序号将权值相加并去除为0的评论序号
        emotional_value = onlyresult.groupby(['index_content'], as_index=False)['weight'].sum()
        emotional_value = emotional_value[emotional_value['weight'] != 0]
        # 取出正面及反面词条
        ind_pos = list(emotional_value[emotional_value['weight'] > 0]['index_content'])
        ind_neg = list(emotional_value[emotional_value['weight'] < 0]['index_content'])
        onlyresult1 = onlyresult[onlyresult['index_content'].isin(ind_pos)]
        onlyresult2 = onlyresult[onlyresult['index_content'].isin(ind_neg)]

        # 画词云图
        frequencies = onlyresult1.groupby(by=['word'])['word'].count()
        frequencies = frequencies.sort_values(ascending=False)
        background_Image = plt.imread(pic_name)
        wordcloud = WordCloud(
            font_path=font_name,
            max_words=100,
            background_color='white',
            mask=background_Image
        )
        my_wordcloud = wordcloud.fit_words(frequencies)
        plt.axis('off')
        plt.imshow(my_wordcloud)
        plt.savefig(write_cloud_name,dpi=600)


if __name__ == "__main__":
    file = pd.read_csv('results/allRightRandom.csv')
    em = DataEmotioner(file)
    em.easysnow_emotion()
    em.store('results/random-right/emotion_label.csv')
    print(em.emaverage)

    # weibodata = pd.read_csv("ALL-data.csv")
    # weibodata2 = pd.read_csv("timesorted-2021.csv")
    # weibodata3 = weibodata2
    # weibodata4 = weibodata3.copy()
    # weibodata4[["content"]].drop_duplicates()
    # content = weibodata3["content"]
    # str_info = re.compile('[0-9a-zA-Z]')
    # content = content.apply(lambda x: str_info.sub('', x))