# 项目内容： 尝试爬取twitter社交平台的数据
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class TwitterSpyder:
    def __init__(self, filename,username, password, keyword):
        self.username = username
        self.password = password
        self.location = filename  # webdriver安装到本地路径来
        self.driver = webdriver.Chrome(executable_path=filename)
        self.url = 'https://twitter.com/'
        self.eng_keyword = keyword

    def login(self):
        self.driver.get(self.url)

        time.sleep(15)
        login = self.driver.find_element_by_xpath('//*[@class="css-901oao r-1awozwy r-13gxpu9 r-6koalj r-18u37iz r-16y2uox r-1qd0xha r-a023e6 r-b88u0q r-1777fci r-rjixqe r-dnmrzs r-bcqeeo r-q4m81j r-qvutc0"]')
        login.click()

        time.sleep(0.5)
        key = self.driver.find_elements_by_xpath(
            '//*[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu"]')

        key[0].send_keys(self.username)
        key[1].send_keys(self.password)

        self.driver.find_element_by_xpath('//*[@class="css-901oao css-16my406 css-bfa6kz r-poiln3 r-bcqeeo r-qvutc0"]').click()

        time.sleep(70)

        # 中间不需要手机输入验证码
        search = self.driver.find_element_by_xpath('//*[@aria-label="Search query"]')
        # 输入搜索内容，回车
        search.send_keys(self.eng_keyword)
        search.send_keys(Keys.ENTER)
        time.sleep(1)

    def getTopComments(self):
        try:
            for i in range(70):
                js = "var q=document.documentElement.scrollTop=10000"
                self.driver.execute_script(js)
                time.sleep(3)  # 加载Ajax
        except:
            pass

        js = "var q=document.documentElement.scrollTop=0"
        self.driver.execute_script(js)  # 拉回上面去

        userName = self.driver.find_elements_by_xpath('//*[@class="css-1dbjc4n r-1awozwy r-18u37iz r-1wbh5a2 r-dnmrzs r-1ny4l3l"]')
        userComments = self.driver.find_elements_by_xpath('//*[@class="css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0"]')
        userTime = self.driver.find_elements_by_xpath('//*[@class="css-4rbku5 css-18t94o4 css-901oao r-m0bqgq r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0"]')
        for i in len(range(userName)):
            print(userName[i].text)
            print(userComments[i].text)
            print(userTime[i].text)

        # print(len(userName), len(userComments), len(userTime))


    def getLatestComments(self):
        time.sleep(1)
        latest = self.driver.find_element_by_xpath('//*[@class= "css-901oao r-m0bqgq r-6koalj r-eqz5dr r-1qd0xha r-a023e6 r-b88u0q r-1pi2tsx r-rjixqe r-bcqeeo r-1l7z4oj r-95jzfe r-bnwqim r-qvutc0"]') # 第一个节点，单击
        latest.click()
        time.sleep(1.1)
        js = "var q=document.documentElement.scrollTop=500000"

        users = self.driver.find_elements_by_xpath('//*[@class="css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l"]')

        wait = WebDriverWait(self.driver, 25)
        try:
            for i in range(30):
                self.driver.execute_script(js)
                time.sleep(5)  # 加载Ajax
                userNames = wait.until(EC.presence_of_all_elements_located(By.XPATH,'//*[@class="css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l"]'))
                if len(userNames) == len(users):
                    users = userNames
                    break
                else:
                    users = userNames
        except Exception as e:
            e.with_traceback()
            print(e)

        print('user字段节点总共获取到',len(users),'条')

        js = "var q=document.documentElement.scrollTop=0"
        self.driver.execute_script(js)  # 拉回上面去
        time.sleep(5)
        try:
            userName = self.driver.find_elements_by_xpath(
                '//*[@class="css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l"]')


            userComments = self.driver.find_elements_by_xpath(
                '//*[@class="css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0"]')
            userTime = self.driver.find_elements_by_xpath(
                '//*[@class="css-4rbku5 css-18t94o4 css-901oao r-m0bqgq r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0"]')
            for i in range(len(userName)):
                print(userName[i].text)
                print(userComments[i].text)
                print(userTime[i].text)
        except Exception as e:
            print(e)
            pass

    def store_mongoDB(self, textlist, text_name, text_time):
        '''数据存入mongoDB'''
        import pymongo
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client['twitter']
        dbcollection = db['twitter']
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
    t = TwitterSpyder(r'F:\Social-Web-Mining\chromedriver.exe','1905720463@qq.com','ATOMBOMB123abc', 'Nuclear sewage')
    t.login()
    t.getLatestComments()
