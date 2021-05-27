# appium 爬取微信的相关信息数据
# https://weixin.sogou.com/ 通过搜狗平台调用微信公众号的数据内容
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

today = datetime.datetime.today()

class WechatSpyder:
    def __init__(self, filename, key):
        self.url = 'https://weixin.sogou.com/'
        self.key = key
        self.filename = filename
        self.driver = webdriver.Chrome(executable_path=filename)  # Chrome Webdriver

    def login(self):
        '''注意： 需要扫码'''
        self.driver.get(self.url)
        login_label = self.driver.find_element_by_id('loginBtn')
        login_label.click()
        time.sleep(20)
        # yh
        wait = WebDriverWait(self.driver, 5) #显式等待
        input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yh')))

        keyword = self.driver.find_element_by_xpath('//*[@class="query"]')
        keyword.send_keys(self.key)

        enter = self.driver.find_element_by_xpath('//*[@class="swz"]')
        enter.click()

    def spy(self):
        wait = WebDriverWait(self.driver, 10)  # 显式等待
        input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'wrapper')))

        next = self.driver.find_elements_by_xpath('//*[@id="sogou_next"]')
        while not next == []:
            textlist = []
            text_name = []
            text_time = []
            sbing = self.driver.find_elements_by_xpath('//*[@class="txt-box"]')
            text_name_list = self.driver.find_elements_by_xpath('//*[@class="account"]')
            text_time_list = self.driver.find_elements_by_xpath('//*[@class="s2"]')


            for item in range(len(sbing)):
                textlist.append(sbing[item].text)
                text_name.append(text_name_list[item].text)
                if text_time_list[item].text[-2:] =='天前':
                    k = (
                        (datetime.datetime.now() - datetime.timedelta(days=int(text_time_list[item].text[:-2]))).strftime(
                            "%Y-%m-%d"))
                    text_time.append(k)

                elif text_time_list[item].text[-3:] =='小时前' or text_time_list[item].text[-3:] == '分钟前':

                    k = (
                        (datetime.datetime.now()).strftime("%Y-%m-%d"))

                    text_time.append(k)
                else:
                    text_time.append(text_time_list[item].text)


            # print(textlist)
            # print(text_time)
            self.store_mongoDB(textlist, text_name, text_time)
            next[0].click()
            time.sleep(2)
            next = self.driver.find_elements_by_xpath('//*[@id="sogou_next"]')



    def store_mongoDB(self, textlist, text_name, text_time):
        '''数据存入mongoDB'''
        import pymongo
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client['wechat']
        dbcollection = db['Wechat']
        # dbcollection.insert_many()
        for i in range(len(textlist)):
            data = {
                'content': textlist[i],
                'author': text_name[i],
                'time': text_time[i]
            }
            dbcollection.insert_one(data)
        print('OK')



if __name__ == '__main__':
    wechat = WechatSpyder(r'F:\Social-Web-Mining\chromedriver.exe', '核污染')
    wechat.login()
    wechat.spy()