# 今日头条数据爬取
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as DC
import requests
import time
import datetime
# 获取今天(现在时间)
today = datetime.datetime.today()
# 昨天


class ToutiaoSpyder:
    def __init__(self, filename, key):
        self.filename = filename
        self.key = key
        self.url = 'https://so.toutiao.com/'
        # self.queryurl = 'https://www.zhihu.com/search?type=content&q=%E6%A0%B8%E5%BA%9F%E6%B0%B4'
        self.driver = webdriver.Chrome(executable_path=filename)  # Chrome Webdriver

        self.textlist = []
        self.text_name = []
        self.text_time = []

    def enter_key(self) -> None:
        try:
            self.driver.get(self.url)
            inputname = self.driver.find_element_by_xpath('//*[@class="input_4uWsU5"]')
            inputname.send_keys(self.key)

            enter = self.driver.find_element_by_xpath('//*[@class="search_1sPyO_"]')
            enter.click()
        except Exception as e:

            print("Error: ", e)
            print("Login Timeout......")
        finally:
            print('End Login!\n')

    def getSpyNews(self) -> None:
        '''
        爬取相关资讯的信息，进入相关的网址
        :return:
        '''
        f = self.driver.find_elements_by_xpath('//*[@class="cs-view cs-view-block cs-tabs-tab"]')[1]
        f.click()

        # 写入相关的数据库，这里写入我们的MongoDB


        #
        next =self.driver.find_elements_by_xpath('//*[@class="position-relative text-ellipsis d-flex align-items-center justify-content-center"]')[-1]

        while next.text == '下一页':

            sbing = self.driver.find_elements_by_xpath('//*[@class="cs-view cs-view-block cs-card-content"]')
            for item in range(len(sbing)):
                lists = str.split(sbing[item].text)
                if not lists[-1] == '西瓜视频':
                    if lists[-2] == '昨天':
                        lists[-1] = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")+" "+lists[-1]
                        self.text_name.append(lists[-4])
                        self.text_time.append(lists[-1])
                        self.textlist.append(''.join(lists[:-4]))

                    elif lists[-2] == '前天':
                        lists[-1] = (today - datetime.timedelta(days=2)).strftime("%Y-%m-%d")+" "+lists[-1]
                        self.text_name.append(lists[-4])
                        self.text_time.append(lists[-1])
                        self.textlist.append(''.join(lists[:-4]))

                    else:
                        if lists[-1][-2:] == '天前':
                            lists[-1] = (
                                (datetime.datetime.now() - datetime.timedelta(days=int(lists[-1][:-2]))).strftime(
                                    "%Y-%m-%d %H:%M"))
                        if lists[-1][-3:] == '分钟前':
                            lists[-1] = ((datetime.datetime.now()-datetime.timedelta(minutes=int(lists[-1][:-3]))).strftime("%Y-%m-%d %H:%M"))
                        if lists[-1][-3:] == '小时前':
                            lists[-1] = ((datetime.datetime.now()-datetime.timedelta(hours=int(lists[-1][:-3]))).strftime("%Y-%m-%d %H:%M"))

                        lists[-1] = lists[-1].replace('年','-').replace('月','-').replace('日','')

                        self.text_name.append(lists[-3])
                        self.text_time.append(lists[-1])
                        self.textlist.append(''.join(lists[:-3]))
            next.click()

            wait = WebDriverWait(self.driver, 10)
            input = wait.until(DC.presence_of_element_located((By.CLASS_NAME, 'search_1sPyO_')))
            next = self.driver.find_elements_by_xpath(
                '//*[@class="position-relative text-ellipsis d-flex align-items-center justify-content-center"]')[-1]

    def getSpyMicro(self):
        '''
        爬取相关讨论的信息（微头条）
        :return:
        '''
        f = self.driver.find_elements_by_xpath('//*[@class="cs-view cs-view-block cs-tabs-tab"]')[6]
        f.click()

        # 写入相关的数据库，这里写入我们的MongoDB


        #
        next =self.driver.find_elements_by_xpath('//*[@class="position-relative text-ellipsis d-flex align-items-center justify-content-center"]')[-1]

        while next.text == '下一页':

            sbing = self.driver.find_elements_by_xpath('//*[@class="d-flex align-items-center text-ellipsis margin-right-4 text-darker"]')
            content = self.driver.find_elements_by_xpath('//*[@class="text-underline-hover"]')
            timelist = self.driver.find_elements_by_xpath('//*[@class="cs-view cs-view-block cs-text-split text-ellipsis text-light text-s"]')
            for item in range(len(sbing)):
                self.text_name.append(sbing[item].text)
                self.textlist.append(content[item+1].text)

                if '·' in timelist[item].text:
                    s = str.split(timelist[item].text, '·')[0]
                    # print(s)
                else:
                    s = timelist[item].text
                lists = str.split(s, ' ')

                if lists[0] == '昨天':
                    lists[-1] = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d") + " " + lists[-1]

                elif lists[0] == '前天':
                    lists[-1] = (today - datetime.timedelta(days=2)).strftime("%Y-%m-%d") + " " + lists[-1]

                else:
                    if lists[-1][-2:] == '天前':
                        lists[-1] = (
                            (datetime.datetime.now() - datetime.timedelta(days=int(lists[-1][:-2]))).strftime(
                                "%Y-%m-%d %H:%M"))
                    if lists[-1][-3:] == '分钟前':
                        lists[-1] = (
                            (datetime.datetime.now() - datetime.timedelta(minutes=int(lists[-1][:-3]))).strftime(
                                "%Y-%m-%d %H:%M"))
                    if lists[-1][-3:] == '小时前':
                        lists[-1] = ((datetime.datetime.now() - datetime.timedelta(hours=int(lists[-1][:-3]))).strftime(
                            "%Y-%m-%d %H:%M"))

                    lists[-1] = lists[-1].replace('年', '-').replace('月', '-').replace('日', '')
                self.text_time.append(lists[-1])

            next.click()

            wait = WebDriverWait(self.driver, 10)
            input = wait.until(DC.presence_of_element_located((By.CLASS_NAME, 'search_1sPyO_')))
            next = self.driver.find_elements_by_xpath(
                '//*[@class="position-relative text-ellipsis d-flex align-items-center justify-content-center"]')[-1]

        print(self.textlist)
        print(self.text_name)
        print(self.text_time)



    def getDiscussions(self):
        '''
        爬取评论的问答情况
        :return:
        '''
        # 看不到用户名，暂时不爬了
        pass

    def store_mongoDB(self):
        import pymongo
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client['toutiao']
        dbcollection = db['toutiao']
        #dbcollection.insert_many()
        for i in range(len(self.textlist)):
            data = {
                'content':self.textlist[i],
                'author':self.text_name[i],
                'time': self.text_time[i]
            }
            dbcollection.insert_one(data)
        print('OK')

if __name__ == '__main__':
    toutiao = ToutiaoSpyder(r'F:\Social-Web-Mining\chromedriver.exe','核废水')
    toutiao.enter_key()
    toutiao.getSpyNews()
    toutiao.getSpyMicro()
    toutiao.store_mongoDB()