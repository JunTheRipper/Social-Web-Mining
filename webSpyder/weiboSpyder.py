# -*- coding: utf-8 -*-
import time
import datetime
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import xlwt

# 先调用无界面浏览器Chrome
# driver = webdriver.Chrome()
# 下载chrome：https://www.google.cn/intl/zh-CN/chrome/
# 要使用Chrome浏览器，必须得有chromedriver
# 并且需要设置环境变量PATH
# 参考：https://www.cnblogs.com/lfri/p/10542797.html
# 如89.0.4389.90版本的chrome对应下载89.0.4389.23即可
# driver = webdriver.Chrome()

class WeiboSpyder:
    def __init__(self, username, password, path, start_y, start_m, start_d, end_y, end_m, end_d, filename):
        self.username = username
        self.password = password
        self.location = path # webdriver安装到本地路径来
        self.driver = webdriver.Chrome(executable_path = path)
        self.start_y = start_y
        self.start_m = start_m
        self.start_d = start_d
        self.end_y = end_y
        self.end_m = end_m
        self.end_d = end_d
        self.filename = filename
        self.sheet = None
        self.page = 0
        self.outfile = None
        self.row = 0
        self.start_stamp = None


    def LoginWeibo(self):
        try:
            # 输入用户名/密码登录
            print('准备登陆Weibo.cn网站...')
            self.driver.get("http://login.sina.com.cn/")
            elem_user = self.driver.find_element_by_name("username")
            elem_user.send_keys(self.username)  # 用户名
            elem_pwd = self.driver.find_element_by_name("password")
            elem_pwd.send_keys(self.password)  # 密码
            elem_sub = self.driver.find_element_by_xpath("//input[@class='W_btn_a btn_34px']")
            elem_sub.click()
            # 点击登陆 因无name属性
            try:
                # 输入验证码
                time.sleep(35)
                elem_sub.click()
            except:
                # 不用输入验证码
                pass

            # 获取Coockie 推荐资料：http://www.cnblogs.com/fnng/p/3269450.html
            print('Crawl in ', self.driver.current_url)
            print('输出Cookie键值对信息:')
            for cookie in self.driver.get_cookies():
                print(cookie)
                for key in cookie:
                    print(key, cookie[key])
            print('登陆成功...')
        except Exception as e:
            print("Error: ", e)
        finally:
            print('End LoginWeibo!\n')

# ********************************************************************************
#                  第二步: 访问http://s.weibo.com/页面搜索结果
#               输入关键词、时间范围，得到所有微博信息、博主信息等
#                     考虑没有搜索结果、翻页效果的情况
# ********************************************************************************

    def GetSearchContent(self, key):
        self.driver.get("http://s.weibo.com/")
        print('搜索热点主题：')

        # 输入关键词并点击搜索
        item_inp = self.driver.find_element_by_xpath("//input[@type='text']")
        #item_inp = driver.find_element_by_xpath("//*[@id='pl_homepage_search']/div/div[2]/div/input")
        item_inp.send_keys(key)
        item_inp.send_keys(Keys.RETURN)  # 采用点击回车直接搜索

        time.sleep(5)
        # 获取搜索词的URL，用于后期按时间查询的URL拼接
        current_url = self.driver.current_url
        current_url = current_url.split('&')[0]  # http://s.weibo.com/weibo/%25E7%258E%2589%25E6%25A0%2591%25E5%259C%25B0%25E9%259C%2587

        # global start_stamp
        #global page


        # 需要抓取的开始和结束日期，可根据你的实际需要调整时间
        start_date = datetime.datetime(self.start_y, self.start_m, self.start_d)
        end_date = datetime.datetime(self.end_y, self.end_m, self.end_d)
        delta_date = datetime.timedelta(days=1)

        # 每次抓取一天的数据
        self.start_stamp = start_date
        end_stamp = start_date + delta_date


        # global sheet

        self.outfile = xlwt.Workbook(encoding='utf-8')

        while end_stamp <= end_date:
            self.page = 1

            # 每一天使用一个sheet存储数据
            self.sheet = self.outfile.add_sheet(self.start_stamp.strftime("%Y-%m-%d-%H"))
            self.initXLS()

            # 通过构建URL实现每一天的查询
            url = current_url + '&typeall=1&suball=1&timescope=custom:' + self.start_stamp.strftime(
                    "%Y-%m-%d-%H") + ':' + end_stamp.strftime("%Y-%m-%d-%H") + '&Refer=g'
            self.driver.get(url)
            self.handlePage()  # 处理当前页面内容
            self.start_stamp = end_stamp
            end_stamp = end_stamp + delta_date


# time.sleep(1)

# ********************************************************************************
#                  辅助函数，考虑页面加载完成后得到页面所需要的内容
# ********************************************************************************

# 页面加载完成后，对页面内容进行处理
    def handlePage(self):
        while True:
            # 之前认为可能需要sleep等待页面加载，后来发现程序执行会等待页面加载完毕
            # sleep的原因是对付微博的反爬虫机制，抓取太快可能会判定为机器人，需要输入验证码
            time.sleep(1)
            # 先行判定是否有内容
            if self.checkContent():
                print("getContent")
                self.getContent()
                # 先行判定是否有下一页按钮
                if self.checkNext():
                    # 拿到下一页按钮
                    next_page_btn = self.driver.find_element_by_css_selector("#pl_feedlist_index > div.m-page > div > a.next")
                    next_page_btn.click()
                else:
                    print("no Next")
                    break
            else:
                print("no Content")
                break


    # 判断页面加载完成后是否有内容
    def checkContent(self):
        # 有内容的前提是有“导航条”？错！只有一页内容的也没有导航条
        # 但没有内容的前提是有“pl_noresult”
        try:
            self.driver.find_element_by_xpath("//div[@class='card card-no-result s-pt20b40']")
            flag = False
        except:
            flag = True
        return flag


# 判断是否有下一页按钮
    def checkNext(self):
        try:
            self.driver.find_element_by_css_selector("#pl_feedlist_index > div.m-page > div > a.next")
            flag = True
        except:
            flag = False
        return flag


# 判断是否有展开全文按钮
    def checkqw(self):
        try:
            self.driver.find_element_by_xpath(".//div[@class='content']/p[@class='txt']/a")
            flag = True
        except:
            flag = False
        return flag


# 在添加每一个sheet之后，初始化字段
    def initXLS(self):
        name = ['博主昵称', '博主主页', '微博认证', '微博达人', '微博内容', '发布位置', '发布时间', '微博地址', '微博来源', '转发', '评论', '赞']

        # global row
        # global outfile


        self.row = 0
        for i in range(len(name)):
            self.sheet.write(self.row, i, name[i])
        self.row = self.row + 1
        self.outfile.save(self.filename)   ############


    # 将dic中的内容写入excel
    def writeXLS(self,dic):
        # global row
        # global outfile


        for k in dic:
            for i in range(len(dic[k])):
                self.sheet.write(self.row, i, dic[k][i])
            self.row = self.row + 1
        self.outfile.save(self.filename)   #############


# 在页面有内容的前提下，获取内容
    def getContent(self):
        # 寻找到每一条微博的class
        try:
            nodes = self.driver.find_elements_by_xpath("//div[@class='card-wrap']/div[@class='card']")
        except Exception as e:
            print(e)

        # 在运行过程中微博数==0的情况，可能是微博反爬机制，需要输入验证码
        if len(nodes) == 0:
            input("请在微博页面输入验证码！")
            url = self.driver.current_url
            self.driver.get(url)
            self.getContent()
            return

        dic = {}


        print(self.start_stamp.strftime("%Y-%m-%d-%H"))
        print('页数:', self.page)
        self.page = self.page + 1
        print('微博数量', len(nodes))

        for i in range(len(nodes)):
            dic[i] = []
            try:
                BZNC = nodes[i].find_element_by_xpath(".//div[@class='content']/p[@class='txt']").get_attribute("nick-name")
            except:
                BZNC = ''
            print('博主昵称:', BZNC)
            dic[i].append(BZNC)

            try:
                BZZY = nodes[i].find_element_by_xpath(".//div[@class='content']/div[@class='info']/div[2]/a").get_attribute("href")
            except:
                BZZY = ''
            print('博主主页:', BZZY)
            dic[i].append(BZZY)
            # 微博官方认证，没有爬取
            try:
                WBRZ = nodes[i].find_element_by_xpath(".//div[@class='info']/div/a[contains(@title,'微博')]").get_attribute('title') # 若没有认证则不存在节点
            except:
                WBRZ = ''
            print('微博认证:', WBRZ)
            dic[i].append(WBRZ)

            try:
                WBDR = nodes[i].find_element_by_xpath(".//div[@class='feed_content wbcon']/a[@class='ico_club']").get_attribute('title')  # 若非达人则不存在节点
            except:
                WBDR = ''
            print('微博达人:', WBDR)
            dic[i].append(WBDR)

            # 判断展开全文和网页链接是否存在
            try:
                nodes[i].find_element_by_xpath(".//div[@class='content']/p[@class='txt']/a[@action-type='fl_unfold']").is_displayed()
                flag = True
            except:
                flag = False
            # 获取微博内容
            try:
                if flag:
                    nodes[i].find_element_by_xpath(".//div[@class='content']/p[@class='txt']/a[@action-type='fl_unfold']").click()
                    time.sleep(1)
                    WBNR = nodes[i].find_element_by_xpath(".//div[@class='content']/p[2]").text.replace("\n","")
                    # 判断发布位置是否存在
                    try:
                        nodes[i].find_element_by_xpath(".//div[@class='content']/p[@class='txt']/a/i[@class='wbicon']").is_displayed()
                        flag = True
                    except:
                        flag = False
                    # 获取微博发布位置
                    try:
                        if flag:
                            pattern = nodes[i].find_elements_by_xpath(".//div[@class='content']/p[2]/a[i[@class='wbicon']]")
                            if isinstance(pattern,list):
                                text = [p.text for p in pattern]
                                FBWZ = [loc for loc in [re.findall('^2(.*$)', t) for t in text] if len(loc) > 0][0][0]
                            else:
                                text = pattern.text
                                FBWZ = re.findall('^2(.*$)',text)[0]
                        else:
                            FBWZ = ''
                    except:
                        FBWZ = ''
                else:
                    WBNR = nodes[i].find_element_by_xpath(".//div[@class='content']/p[@class='txt']").text.replace("\n","")
                    # 判断发布位置是否存在
                    try:
                        nodes[i].find_element_by_xpath(".//div[@class='content']/p[@class='txt']/a/i[@class='wbicon']").is_displayed()
                        flag = True
                    except:
                        flag = False
                    # 获取微博发布位置
                    try:
                        if flag:
                            pattern = nodes[i].find_elements_by_xpath(".//div[@class='content']/p[@class='txt']/a[i[@class='wbicon']]")
                            if isinstance(pattern,list):
                                text = [p.text for p in pattern]
                                FBWZ = [loc for loc in [re.findall('^2(.*$)', t) for t in text] if len(loc) > 0][0][0]
                            else:
                                text = pattern.text
                                FBWZ = re.findall('^2(.*$)',text)[0]
                        else:
                            FBWZ = ''
                    except:
                        FBWZ = ''
            except:
                WBNR = ''
            print('微博内容:', WBNR)
            dic[i].append(WBNR)

            print('发布位置:', FBWZ)
            dic[i].append(FBWZ)

            try:
                FBSJ = nodes[i].find_element_by_xpath(".//div[@class='content']/p[@class='from']/a[1]").text
            except:
                FBSJ = ''
            print('发布时间:', FBSJ)
            dic[i].append(FBSJ)

            try:
                WBDZ = nodes[i].find_element_by_xpath(".//div[@class='content']/p[@class='from']/a[1]").get_attribute("href")
            except:
                WBDZ = ''
            print('微博地址:', WBDZ)
            dic[i].append(WBDZ)

            try:
                ZF_TEXT = nodes[i].find_element_by_xpath(".//a[@action-type='feed_list_forward']").text
                if ZF_TEXT == '转发':
                    ZF = 0
                else:
                    ZF = int(ZF_TEXT.split(' ')[1])
            except:
                ZF = 0
            print('转发:', ZF)
            dic[i].append(ZF)
            print('\n')

        # 写入Excel
        self.writeXLS(dic)


# *******************************************************************************
#                                程序入口
# *******************************************************************************
if __name__ == '__main__':
    # 定义变量
    username = ''  # 输入你的用户名
    password = ''  # 输入你的密码
    path = 'chromedriver.exe'
    weiboSpyder = WeiboSpyder(username, password, path, 2021, 1, 1, 2021, 4, 16,"data")
    # 操作函数
    weiboSpyder.LoginWeibo()  # 登陆微博

    # 搜索热点微博爬取评论
    # 关键词请根据实际需要进行替换
    # 请搜索和疫情有关的一些非敏感关键词
    # 注意：如果输入的是“疫情”“武汉”“中国”这样的敏感词汇，微博不会返回给你任何结果
    # 请尽量输入疫情相关又不会敏感的词汇，可以输入一些疫情支援人员的姓名试试看

    key = '#疫苗#'
    weiboSpyder.GetSearchContent(key)
