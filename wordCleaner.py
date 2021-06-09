import pandas as pd
import jieba
import jieba.analyse
import jieba.posseg as psg
import filestore
# 字符处理器 实现jiaba 分词化和去停用词技术

def duplicate_removal(str1:str)->str:
    list=str1.split(" ")
    temp=[]
    result=''
    for word in list:
        if word not in temp:
            temp.append(word)
    for word in temp:
        result+=word+" "
    return result


class WordCleaner:
    def __init__(self, data:str):
        '''
        :param data: -> pd.DataFrame
        '''
        self.data = data

    def stop_words_data(self, filedir:str) -> pd.DataFrame:
        '''
        :param filedir:  文件存储的路径（注意，是目录）
        :return: dataframe, 便于后续存入mysql或者mongoDB
        '''
        # 设置停用词，构建词频矩阵
        stopwords = []
        for word in open('stopwords/baidu_stopwords.txt', 'r', encoding='utf-8'):
            stopwords.append(word.strip())
        dataCon = self.data['content']
        username = self.data["author"]
        date = self.data["time"]
        part_of_speech = []
        for line in dataCon:
            seg_list = psg.cut(line)

            result = " ".join(["{0}/{1}".format(w, t) for w, t in seg_list])
            part_of_speech.append(result)
        # part_of_speech
        print("分词切割成功！")
        dataframe = pd.DataFrame({'content': part_of_speech, 'author': username, 'time': date})
        dataframe.to_csv(filedir+"/cutdataContent.csv", index=False, sep=',')
        return dataframe

    def jieba_cut(self, filedir:str) -> pd.DataFrame:
        '''

        :param filedir: jieba分词实体集存储路径
        :return: dataframe 实体集列表
        '''
        # 使用jieba进行词性切分，allowPOS指定允许的词性，这里选择名词n和地名ns
        dataCon = self.data['content']
        username = self.data["author"]
        date = self.data["time"]

        dataContent = self.data['content'].values

        whole_list = []
        for line in dataContent:
            line_list = []
            kw = jieba.analyse.extract_tags(line, topK=50, withWeight=True, allowPOS=('n', 'ns'))

            for item in kw:
                line_list.append(item[0])
            whole_list.append(line_list)

        with open(filedir+"/entity.txt", "w+", encoding="utf-8") as f:
            for item in whole_list:
                f.write(str(item) + ',\n')

        dataframe = pd.DataFrame({'content': whole_list, 'author': username, 'time': date})
        dataframe.to_csv(filedir+"/entity.csv", index=False, sep=',')

        print("实体集获取成功！")

        return dataframe


    def data_cut_repeation(self, filedir:str) -> pd.DataFrame:
        '''
        分词处理的数据去除重复值

        :param filedir:  str 文件路径
        :return:  data pd.DataFrame 去除后的DataFrame格式数据
        '''
        authorList = self.data["author"]
        timeList = self.data["time"]
        contentList = self.data["content"]
        for content in contentList:
            content = duplicate_removal(content)

        list = {
            "content": contentList,
            "author": authorList,
            "time": timeList
        }

        data = pd.DataFrame(list)
        # a = filestore.FileStore(self.data, 'dup_CutDataContent')
        # a.download_as_csv()
        data.to_csv(filedir+"/newCutDataContent.csv", index=False)
        return data