# -*- coding: utf-8 -*-
# https://zhihu.sogou.com/ 通过搜狗平台调用微信公众号的数据内容
# 单纯爬知乎会被反爬
import time
import datetime
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as DC
import requests
from bs4 import BeautifulSoup

# 知乎不需要登录，但是有ajax

class ZhiHuSpyder:
    def __init__(self, filename):
        self.filename = filename
        self.url = 'https://www.zhihu.com/topic/19566105/top-answers'
        self.driver = webdriver.Chrome(executable_path=filename) # Chrome Webdriver



    def login(self):
        '''注意： 需要扫码'''
        self.driver.get(self.url)
        login_label = self.driver.find_element_by_id('loginBtn')
        login_label.click()
        time.sleep(20)
        # yh
        wait = WebDriverWait(self.driver, 5)  # 显式等待
        input = wait.until(DC.presence_of_element_located((By.CLASS_NAME, 'yh')))

        keyword = self.driver.find_element_by_xpath('//*[@class="query"]')
        keyword.send_keys(self.key)

        enter = self.driver.find_element_by_xpath('//*[@id="stb"]')
        enter.click()


    def getSpyContent(self) -> None:
        '''注意: 知乎爬取的文章而不是评论'''

        textlist = []
        text_name = []
        text_time = []

        self.driver.get(self.url)
        time.sleep(1)

        try:
            for i in range(70):
                js = "var q=document.documentElement.scrollTop=10000"
                self.driver.execute_script(js)
                time.sleep(1.2)# 加载Ajax
        except:
            pass
        js = "var q=document.documentElement.scrollTop=0"
        self.driver.execute_script(js)  # 拉回上面去

        fin = self.driver.find_elements_by_xpath('//*[@class="UserLink-link"]')


        for i in range(len(fin)):
            try:
                self.driver.execute_script("arguments[0].focus();", fin[i])
                text_name.append(self.driver.find_elements_by_xpath('//*[@class="UserLink-link"]')[i].text)

                full_text = self.driver.find_elements_by_xpath('//*[@class="RichText ztext CopyrightRichText-richText"]')[i]
                self.driver.execute_script("arguments[0].scrollIntoView();", full_text)
                self.driver.execute_script("arguments[0].click();", full_text)

                title = self.driver.find_elements_by_xpath('//*[@class="ContentItem-title"]')[i]

                txt = self.driver.find_elements_by_xpath('//*[@class="RichContent-inner"]')[i]
                textlist.append(title.text+txt.text)

                timeline = self.driver.find_elements_by_xpath('//*[@class="ContentItem-time"]')[i]
                self.driver.execute_script("arguments[0].focus();", timeline)
                text_time.append(str.split(timeline.text, ' ')[1])
            except:
                pass
        self.store_mongoDB(textlist, text_name, text_time)

    def parse(self, html_source_code):
        '''
        :param html_source_code:  html源代码
        :return:
        '''
        with open('D:\\1.html', 'w',encoding='utf-8') as f:
            f.write(html_source_code)

    def getComments(self):
        '''爬取评论数据'''

        self.driver.get(self.url)
        time.sleep(0.5)
        try:
            for i in range(70):
                js = "var q=document.documentElement.scrollTop=10000"
                self.driver.execute_script(js)
                time.sleep(1.2)# 加载Ajax
        except:
            pass
        js = "var q=document.documentElement.scrollTop=0"
        self.driver.execute_script(js)  # 拉回上面去

        # 需要爬取对应的评论和回复

        remark = self.driver.find_elements_by_xpath('//*[@class="Button ContentItem-action Button--plain Button--withIcon Button--withLabel"]')

        for remarkitem in remark:
            textlist = []
            text_name = []
            text_time = []
            try:
                # remark = self.driver.find_element_by_xpath('//*[@class="Button ContentItem-action Button--plain Button--withIcon Button--withLabel"]')
                if remarkitem.text[-3:] == '条评论':

                    self.driver.execute_script("arguments[0].scrollIntoView();", remarkitem)
                    self.driver.execute_script("arguments[0].click();", remarkitem)

                    time.sleep(0.5)

                    next = self.driver.find_elements_by_xpath('//*[@class="Button PaginationButton PaginationButton-next Button--plain"]')

                    while True:

                        comments = self.driver.find_elements_by_xpath('//*[@class="CommentRichText CommentItemV2-content"]')
                        times = self.driver.find_elements_by_xpath('//*[@class="CommentItemV2-time"]')
                        users = self.driver.find_elements_by_xpath('//*[@class="CommentItemV2-meta"]')

                        # 遍历所有评论
                        for i in range(len(comments)):
                            self.driver.execute_script("arguments[0].focus();", comments[i])
                            textlist.append(comments[i].text)
                            text_time.append(times[i].text)
                            string = str.split(users[i].text, '\n')[0]
                            # 处理存在'回复xxx'的数据字段
                            if '回复' in string:
                                strings = str.split(string, '回复')[0]
                            else:
                                strings = string
                            text_name.append(strings)
                            # print(text_name)
                        self.driver.execute_script("arguments[0].focus();", next[-1])

                        self.driver.execute_script("arguments[0].click();", next[-1])

                        time.sleep(0.5)
                        # print(text_name)
                        next = self.driver.find_elements_by_xpath('//*[@class="Button PaginationButton PaginationButton-next Button--plain"]')

                        if len(next) == 0:
                            break
                self.store_mongoDB(textlist, text_name, text_time)
            except Exception as e:
                print('ERROR:', e)
                pass
        print(text_name)
        print('storing into mongoDB......')


    def store_mongoDB(self, textlist, text_name, text_time):
        '''数据存入mongoDB'''
        import pymongo
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client['zhihu']
        dbcollection = db['zhihuComments']
        # dbcollection.insert_many()
        for i in range(len(textlist)):
            data = {
                'content': textlist[i],
                'author': text_name[i],
                'time': text_time[i]
            }
            dbcollection.insert_one(data)
        print('insert one piece......')

if __name__ == '__main__':
    zhihu = ZhiHuSpyder(r'F:\Social-Web-Mining\chromedriver.exe')

    zhihu.getComments()
    # zhihu.getSpyContent()
    # print(ans.text)
