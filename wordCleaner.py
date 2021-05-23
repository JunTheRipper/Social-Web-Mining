import pandas as pd
import jieba
import jieba.analyse
import jieba.posseg as psg

# 字符处理器 实现jiaba 分词化和去停用词技术


class WordCleaner:
    def __init__(self, data):
        '''
        :param data: -> pd.DataFrame
        '''
        self.data = data

    def stop_words_data(self) -> None:
        # 设置停用词，构建词频矩阵
        stopwords = []
        for word in open('stopwords/cn_stopwords.txt', 'r', encoding='utf-8'):
            stopwords.append(word.strip())
        dataCon = self.data['微博内容']
        username = self.data["博主昵称"]
        date = self.data["发布时间"]
        part_of_speech = []
        for line in dataCon:
            seg_list = psg.cut(line)

            result = " ".join(["{0}/{1}".format(w, t) for w, t in seg_list])
            part_of_speech.append(result)
        # part_of_speech
        print("分词切割成功！")
        dataframe = pd.DataFrame({'dataContent': part_of_speech, 'username': username, 'date': date})
        dataframe.to_csv("results/random-nuclear/dataContent.csv", index=False, sep=',')


    def jieba_cut(self) -> None:

        # 使用jieba进行词性切分，allowPOS指定允许的词性，这里选择名词n和地名ns
        dataContent = self.data['微博内容'].values

        whole_list = []
        for line in dataContent:
            line_list = []
            kw = jieba.analyse.extract_tags(line, topK=50, withWeight=True, allowPOS=('n', 'ns'))
            #     print(kw)
            for item in kw:
                line_list.append(item[0])
            whole_list.append(line_list)

        with open("results/random-nuclear/entity.txt", "w+", encoding="utf-8") as f:
            for item in whole_list:
                f.write(str(item) + ',\n')

        print("实体集获取成功！")
