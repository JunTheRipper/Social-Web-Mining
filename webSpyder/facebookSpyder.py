import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class FaceBookSpyder:
    def __init__(self, filename,username, password, keyword):
        self.username = username
        self.password = password
        self.location = filename  # webdriver安装到本地路径来
        self.driver = webdriver.Chrome(executable_path=filename)
        self.url = 'https://www.facebook.com/'
        self.eng_keyword = keyword

    def login(self):

        self.driver.get(self.url)

        time.sleep(15)

        self.driver.maximize_window()
        self.driver.find_element_by_id('email').send_keys(self.username)
        self.driver.find_element_by_id('pass').send_keys(self.password)

        self.driver.find_element_by_name('login').click()
        time.sleep(5)

        wait = WebDriverWait(self.driver, 20)  # 显式等待
        input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="rq0escxv a8c37x1j a5nuqjux l9j0dhe7 k4urcfbm"]')))

        self.driver.find_element_by_xpath('//*[@class="rq0escxv a8c37x1j a5nuqjux l9j0dhe7 k4urcfbm"]').click()
        # 搜索的节点
        time.sleep(0.5)
        self.driver.find_element_by_name('global_typeahead').send_keys(self.eng_keyword)
        # 输入相关关键词 如： nuclear waste 等等
        self.driver.find_element_by_name('global_typeahead').send_keys(Keys.ENTER)

        # 菜单栏选择帖子
        wait = WebDriverWait(self.driver, 20)  # 显式等待
        wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="oajrlxb2 gs1a9yip i224opu6 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 a8c37x1j mg4g778l btwxx1t3 pfnyh3mw p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb lzcic4wl abiwlrkh p8dawk7l ue3kfks5 pw54ja7n uo3d90p7 l82x9zwi"]')))

        self.driver.find_element_by_xpath('//*[@class="oajrlxb2 gs1a9yip i224opu6 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 a8c37x1j mg4g778l btwxx1t3 pfnyh3mw p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb lzcic4wl abiwlrkh p8dawk7l ue3kfks5 pw54ja7n uo3d90p7 l82x9zwi"]').click()

        wait.until(
            EC.presence_of_element_located((By.XPATH,'//*[@class="buofh1pr qzhwtbm6 knvmm38d hpfvmrgz"]')))

        self.driver.find_element_by_xpath('//*[@class="buofh1pr qzhwtbm6 knvmm38d hpfvmrgz"]').click()

        wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="hzawbc8m hyh9befq cehpxlet rs0gx3tq"]')))

        self.driver.find_elements_by_xpath('//*[@class="hzawbc8m hyh9befq cehpxlet rs0gx3tq"]')[-1].click()


    def spy(self):
        textlist = []
        text_name = []
        text_time = []

        # Ajax 加载界面，一直下拉进度条，下拉x次以后遍历爬取数据

        try:
            for i in range(30):
                js = "var q=document.documentElement.scrollTop=500000"
                self.driver.execute_script(js)
                time.sleep(1)
                time.sleep(1)  # 加载Ajax
        except Exception as e:
            print(e)
            pass

        js = "var q=document.documentElement.scrollTop=0"
        self.driver.execute_script(js)  # 拉回上面去


        fin = self.driver.find_elements_by_xpath('//*[@class="rq0escxv l9j0dhe7 du4w35lb j83agx80 cbu4d94t g5gj957u d2edcug0 hpfvmrgz rj1gh0hx buofh1pr p8fzw8mz pcp91wgn iuny7tx3 ipjc6fyt"]')

        name = self.driver.find_elements_by_xpath('//*[@class="a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7 nkwizq5d roh60bw9 hop8lmos scwd0bx6 n8tt0mok hyh9befq jwdofwj8 r8blr3vg"]')

        timeline = self.driver.find_elements_by_xpath('//*[@class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh jq4qci2q a3bd9o3v knj5qynh m9osqain"]')

        print(len(fin), len(name), len(timeline))
        number = 0
        for i in range(len(fin)):
            print(fin[i].text)
            print(name[i].text)

            textlist.append(fin[i].text)
            text_name.append(name[i].text)

        # self.store_mongoDB(textlist, text_name, text_time)

    def store_mongoDB(self, textlist, text_name, text_time):
        '''数据存入mongoDB'''
        import pymongo
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client['facebook']
        dbcollection = db['facebooktopic']
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
    f = FaceBookSpyder(r'F:\Social-Web-Mining\chromedriver.exe','','', 'Nuclear sewage')
    f.login()
    f.spy()