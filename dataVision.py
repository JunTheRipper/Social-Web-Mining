import jieba
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import jieba.analyse


class DataVisitor:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def show_word_cloud(self, font_name:str, pic_name:str, write_name:str,write_cloud_name:str) -> list:
        '''
        :param font_name:  字体存储路径(.ttc)
        :param pic_name:   图片存储路径(.png/.jpg)
        :param write_name:  词频生成路径(.txt)
        :param write_cloud_name:  词云图片生成路径(.png)
        :return:
        '''
        cluster1 = ' '.join(self.data['content'].values)

        kw1 = jieba.analyse.textrank(cluster1, topK=50, withWeight=True, allowPOS=('ns', 'n'))
        words_frequence = {x[0]: x[1] for x in kw1}
        print(words_frequence)
        with open(write_name,'w') as f:
            f.write(str(words_frequence))
        backgroud_Image = plt.imread(pic_name)  # 准备背景样式

        # 若是有中文的话，font_path ='simsun.ttc'必须添加，不然会出现方框，不出现汉字
        # simsun.ttc为汉字编码文件，可以从本地windows系统找一个汉字编码文件上传， 如C:\\Windows\Fonts下有许多汉字编码文件

        wordcloud = WordCloud(font_path=font_name, mask=backgroud_Image, repeat=True, background_color='white')
        wordcloud = wordcloud.fit_words(words_frequence)
        plt.imshow(wordcloud)
        plt.savefig(write_cloud_name,dpi=600)

        return words_frequence