import json
from webSpyder.weiboSpyder import WeiboSpyder
import pandas as pd

with open("intro.json","r",encoding="utf-8") as f:
    json_data = json.load(f)
username = json_data['username']
password = json_data['password']
webdriver_path = json_data['chrome_driver_location']
useremail = json_data['useremail']
data_store_location = json_data['data_store_location']
result_analyse_location = json_data['result_analyse_location']
result_picture = json_data['result_picture']
keyword = json_data['keyword']

#
# weiboSpyder = WeiboSpyder(username, password, webdriver_path, 2021, 5, 17, 2021, 5, 23,"Data/right513.xls")
# weiboSpyder.LoginWeibo()
# weiboSpyder.GetSearchContent(keyword)
import os


# file_list ="Data/weiboSpy"
# from dataProcessing import *
# data = multi_excel_combine(file_list)
# data = drop_nan_data(data)
# show_nan_data(data)
# data = drop_repeat_data(data)
# data = drop_symbols(data)
# data = data_cut_weibo(data)
# write_into_csv(data, 'nuclear.csv')

import wordCleaner
# from wordCleaner import WordCleaner
# data = pd.read_csv("results/random-nuclear/allnuclearRandom.csv",encoding="utf-8")
#
# word = WordCleaner(data)
# word.stop_words_data()
# word.jieba_cut()

from dataVision import DataVisitor
data = pd.read_csv("results/random-nuclear/allnuclearRandom.csv",encoding="utf-8")
dataViewer = DataVisitor(data)
dataViewer.show_word_cloud('material/simsun.ttc', 'material/cat.jpg','results/random-nuclear/word_frequency.txt', 'results/random-nuclear/cat_cloud.png')