import jieba
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import jieba.analyse
import os

class DataVisitor:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def show_word_cloud(self, font_name:str, pic_name:str,
                        write_name:str,write_cloud_name:str) -> list:
        '''
        :param font_name:  字体存储路径(.ttc)
        :param pic_name:   图片存储路径(.png/.jpg)
        :param write_name:  词频生成路径(.txt)
        :param write_cloud_name:  词云图片生成路径(.png)
        :return:
        '''
        cluster1 = ' '.join(self.data['content'].values)

        kw1 = jieba.analyse.textrank(cluster1, topK=50,
                                     withWeight=True, allowPOS=('ns', 'n'))
        words_frequence = {x[0]: x[1] for x in kw1}
        print(words_frequence)
        with open(write_name,'w') as f:
            f.write(str(words_frequence))
        backgroud_Image = plt.imread(pic_name)  # 准备背景样式

        # 若是有中文的话，font_path ='simsun.ttc'必须添加，不然会出现方框，不出现汉字
        # simsun.ttc为汉字编码文件，可以从本地windows系统找一个汉字编码文件上传，
        # 如C:\\Windows\Fonts下有许多汉字编码文件

        wordcloud = WordCloud(font_path=font_name,
                              mask=backgroud_Image, repeat=True,
                              background_color='white')
        wordcloud = wordcloud.fit_words(words_frequence)
        plt.imshow(wordcloud)
        plt.savefig(write_cloud_name,dpi=600)

        return words_frequence

    def mapDrawer(self, start_y: int, start_m: int, start_d: int,
                  end_y: int, end_m: int, end_d: int, delta_d: int, key: str, write_location: str):
        '''
        丁香园类地图时序绘制模块，实现pyecharts的关键内容绘制
        :return: html网页格式的数据结果
        '''
        import pandas as pd
        import pyecharts.options as opts
        from pyecharts.globals import ThemeType
        from pyecharts.commons.utils import JsCode
        from pyecharts.charts import Timeline, Grid, Bar, Map, Pie, Line
        import datetime


        # print(df_dxy)

        StartDay = datetime.date(start_y, start_m, start_d)
        EndDay = datetime.date(end_y, end_m, end_d)
        OneDay = datetime.timedelta(days=delta_d)
        time_list = []
        while StartDay < EndDay:
            StartDay += OneDay
            time_list.append(''.join(str(StartDay)))
        # print(time_list)
        # time_list = df_dxy["Date"].values[0:121]
        maxNum = 40000
        minNum = 0
        timeline = Timeline(
            init_opts=opts.InitOpts(width="1600px", height="900px", theme=ThemeType.DARK)
        )
        for j in time_list:
            Date1 = self.data[self.data['日期'] == j]
            list1 = []
            list2 = []
            for i in Date1["市"]:
                i = i + "市"
                list1.append(i)
            for i, k in zip(Date1["确诊"], Date1["治愈"]):
                list2.append(i - k)

            map_data = list(zip(list1, list2))

            map = Map(opts.InitOpts(width="1600px", height="900px")).add(
                series_name=key+"疫情发展趋势",
                data_pair=map_data,
                maptype=key,
                is_map_symbol_show=False
            )
            map.set_global_opts(title_opts=opts.TitleOpts(title=key+"疫情分布"),
                                visualmap_opts=opts.VisualMapOpts(max_=maxNum, is_piecewise=True))
            timeline.add(map, time_point=str(j))
        timeline.add_schema(
            orient="vertical",
            is_auto_play=True,
            is_inverse=True,
            play_interval=100,
            pos_left="null",
            pos_right="5",
            pos_top="20",
            pos_bottom="20",
            width="60",
            label_opts=opts.LabelOpts(is_show=True, color="#fff"),
        )

        timeline.render(write_location)
        os.system(write_location) # 启动显示



if __name__ == '__main__':
    df_dxy = pd.read_csv("Data/DXYData/DXYdata.csv", index_col=False)
    df_dxy = df_dxy[df_dxy["省"] == "湖北省"]
    df_dxy.reset_index(drop=True, inplace=True)

    vis = DataVisitor(df_dxy)
    vis.mapDrawer(2020, 1, 22, 2020, 3, 18, 1, "湖北", 'results/random-DXY/DXY.html')