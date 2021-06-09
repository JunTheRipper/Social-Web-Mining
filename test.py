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
weiboSpyder = WeiboSpyder(username, password, webdriver_path, 2018, 10, 1, 2020, 12, 30,"Data/tt.xls")
weiboSpyder.LoginWeibo()
weiboSpyder.GetSearchContent(keyword)
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

# from dataVision import DataVisitor
# data = pd.read_csv("results/random-nuclear/allnuclearRandom.csv",encoding="utf-8")
# dataViewer = DataVisitor(data)
# dataViewer.show_word_cloud('material/simsun.ttc', 'material/cat.jpg','results/random-nuclear/word_frequency.txt', 'results/random-nuclear/cat_cloud.png')
#
# import pandas as pd
# import dataProcessing as dp
#
# excelData = data_store_location+'/excelData'
# mongoData = data_store_location+'/mongoData'
# otherData = data_store_location+'/otherData'
#
# excel = dp.multi_excel_combine(excelData)
# mongo = dp.multi_csv_combine(mongoData)
# other = dp.multi_csv_combine(otherData)
# print(excel.shape)
# print(mongo.shape)
# print(other.shape)
# print("whole raw data: ",excel.shape[0]+mongo.shape[0]+other.shape[0])
#
# # 集体去重,先处理微博的情况
# df_weibo_excel = dp.data_renameweibo(excel)
# df_weibo_other = dp.data_renameweibo(other)
#
# # 对excel和other下的微博数据集体抽取并合并起来
# dfA = dp.data_cut(df_weibo_excel)
# dfB = dp.data_cut(df_weibo_other)
# mg = dp.data_cut(mongo)
#
# dfAB = dp.multi_pd_combine(dfA, dfB)
# dfABC = dp.multi_pd_combine(dfAB, mg)
# print(dfABC.head())

import filestore as fs
a = fs.FileStore('processed-content-data')
a.download_as_csv()