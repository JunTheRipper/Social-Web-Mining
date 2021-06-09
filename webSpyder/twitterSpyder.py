# 项目内容： 尝试爬取twitter社交平台的数据
# 调用gitHub上的相关项目实现
import datetime
import time
from concurrent.futures import ThreadPoolExecutor
import requests
from selenium import webdriver
import pandas as pd

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# try:
#     from DBUtils.PooledDB import PooledDB
# except ImportError:
#     from dbutils.pooled_db import PooledDB

df = pd.DataFrame(columns=['user_id','user_name','day','created_time','tweet_text','comment_count','share_count','like_count'])

headers = {
    'authority': 'api.twitter.com',
    'x-twitter-client-language': 'en-US',
    'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'sec-fetch-dest': 'empty',
    'x-guest-token': 'bee93f99ee1751e34cd91889c0e7eab05e3aa3c9a4bb034fc9377af357b351064dcb3508fa5e0bdc3ce9f4ba4037b13bfec1eb3423f5a25b9cf65c4e3b84d83a0798ab35300671d661891acdaa5db911',
    'x-twitter-active-user': 'yes',
    'accept': '*/*',
    'origin': 'https://www.twitter.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
}
url = "https://api.twitter.com/2/search/adaptive.json"
# dbpool = PooledDB(creator=pymysql, mincached=10, maxcached=10, maxshared=20, maxconnections=100,
#                   host='localhost', user='root', passwd='123456', db='twitter', port=3306, charset='utf8mb4')


class Tweet():
    cnt = 0
    total = 0

    def __init__(self, tweet_id, user_id, user_name, created_time, tweet_text, comment_count, share_count, like_count):
        self.tweet_id = tweet_id
        format_str = '%a %b %d %H:%M:%S +0000 %Y'
        utcdatetime = time.strptime(created_time, format_str)
        self.user_id = user_id
        self.user_name = user_name.replace(u'\xa0', u' ')
        self.user_name = bytes(
            self.user_name, 'utf-8').decode('utf-8', 'ignore')
        self.day = created_time = time.strftime("%Y-%m-%d", utcdatetime)
        self.created_time = time.strftime("%Y-%m-%d %H:%M:%S", utcdatetime)
        self.tweet_text = tweet_text.replace(u'\xa0', u' ')
        self.tweet_text = bytes(
            self.tweet_text, 'utf-8').decode('utf-8', 'ignore')
        self.comment_count = comment_count
        self.share_count = share_count
        self.like_count = like_count

    def write(self):
        Tweet.cnt += 1
        Tweet.total+=1
        # conn = dbpool.connection()
        # cur = conn.cursor()
        # sql = "REPLACE INTO search_tweet(tweet_id, user_id, user_name, created_time, tweet_text,comment_count,share_count,like_count)VALUES (%s, %s, %s, %s, %s,%s,%s,%s)"
        # arg = [self.tweet_id, self.user_id, self.user_name, self.created_time,
        #        self.tweet_text, self.comment_count, self.share_count, self.like_count]
        # cur.execute(sql, arg)
        # conn.commit()
        # conn.close()
        info = [self.user_id,self.user_name,self.day,self.created_time,self.tweet_text,self.comment_count,self.share_count,self.like_count]
        df.loc[df.shape[0]]=info
        if self.total%1000==0:
            print(self.total, "write successful")
        #df.to_csv("out.csv")
        #print(self.tweet_text)


class TwitterSearch(object):
    def __init__(self, query, maxTweets, day, driverpath):
        self.passcnt = 100
        self.stopflag = -1
        self.maxTweets = maxTweets
        self.day = day
        self.driverpath = driverpath
        self.params = {
            'include_profile_interstitial_type': '1',
            'include_blocking': '1',
            'include_blocked_by': '1',
            'include_followed_by': '1',
            'include_want_retweets': '1',
            'include_mute_edge': '1',
            'include_can_dm': '1',
            'include_can_media_tag': '1',
            'skip_status': '1',
            'cards_platform': 'Web-12',
            'include_cards': '1',
            'include_composer_source': 'true',
            'include_ext_alt_text': 'true',
            'include_reply_count': '1',
            'tweet_mode': 'extended',
            'include_entities': 'true',
            'include_user_entities': 'true',
            'include_ext_media_color': 'true',
            'include_ext_media_availability': 'true',
            'send_error_codes': 'true',
            'simple_quoted_tweets': 'true',
            'tweet_search_mode': 'live',
            'count': '10',
            'query_source': 'typed_query',
            'pc': '1',
            'spelling_corrections': '1',
            'ext': 'mediaStats,highlightedLabel,cameraMoment',
            "q": query
        }

    def spider(self):
        if(self.maxTweets != None and Tweet.cnt > self.maxTweets):
            return
        while self.stopflag and self.passcnt > 0:
            try:
                response = requests.get(url, headers=headers, params=self.params,timeout=20)
                jsonData = response.json()
                self.edit_params(jsonData)
                self.parse_tweets(jsonData)
            except requests.exceptions.RequestException as e:
                print(e)
                self.passcnt-=1

    def parse_tweets(self, jsonData):
        #  tweet_id, user_id, user_name, created_time, tweet_text
        contents = jsonData.get("globalObjects").get("tweets")
        users = jsonData.get("globalObjects").get("users")
        for info in contents.values():
            tweet_id = info.get("id_str")
            user_id = info.get("user_id_str")
            user_name = users.get(user_id).get("name")
            created_time = info.get("created_at")
            tweet_text = info.get("full_text")
            comment_count = info.get("reply_count")
            share_count = info.get("retweet_count")
            like_count = info.get("favorite_count")
            tweet = Tweet(tweet_id, user_id, user_name,
                          created_time, tweet_text, comment_count, share_count, like_count)
            if(self.day != tweet.day):
                # print(tweet.tweet_id, "pass!!!")
                self.passcnt -= 1
                continue
            if(self.maxTweets != None and Tweet.cnt > self.maxTweets):
                print("达到次数上限")
                self.stopflag = 0
                Tweet.cnt = 0
                return False
            else:
                tweet.write()

    def edit_params(self, jsonData):
        instructions = jsonData.get("timeline").get("instructions")
        if self.stopflag == -1:
            scrollCursorValue = instructions[0].get("addEntries").get("entries")[-1].get("content").get(
                "operation").get("cursor").get("value")
            self.params['cursor'] = scrollCursorValue
            self.stopflag = 1
        else:
            try:
                scrollCursorValue = instructions[-1].get("replaceEntry").get("entry").get("content").get("operation").get(
                    "cursor").get("value")
                if self.params['cursor'] != scrollCursorValue:
                    self.params['cursor'] = scrollCursorValue
                else:
                    self.stopflag = 0
            except:
                self.stopflag = 0

    @staticmethod
    def creat_query(keyword, since, until, lang):
        query = keyword + ' until:{} since:{}'.format(until, since)
        if lang:
            languages = {1: 'en', 2: 'it', 3: 'es',
                         4: 'fr', 5: 'de', 6: 'ru', 7: 'zh'}
            query += " lang:{}".format(languages[lang])
        return query

    @staticmethod
    def init_headers(path):
        print("#############获取token##############")
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        option.add_argument('--lang=zh-cn')
        option.add_argument('--ignore-certificate-errors')
        browser = webdriver.Chrome(options=option, executable_path=path)

        browser.get("https://twitter.com/search")
        cookiesList = browser.get_cookies()
        cookies = {}
        for cookie in cookiesList:
            cookies[cookie.get("name")] = cookie.get("value")
        browser.quit()
        print("cookies", cookies)
        headers["x-guest-token"] = cookies['gt']

        print(cookies['gt'])
        print("##############获取token成功###########")


class MultiThread:
    """
    Class of make get tweets by python threading
    """

    def __init__(self, keyword, since, until, lang, max_tweets, chromedriverpath,  n_threads=1):
        self.keyword = keyword
        self.since = since
        self.until = until
        self.max_tweets = max_tweets
        self.n_threads = n_threads
        self.path = chromedriverpath
        self.lang = lang

    def search_thread(self):
        """
        :param query:
        :param lang: Choose a language to set get tweets's language
        :return:
        """
        TwitterSearch.init_headers(self.path)
        n_days = (self.until - self.since).days
        tp = ThreadPoolExecutor(max_workers=self.n_threads)
        for i in range(n_days, -1, -1):
            since = self.since + datetime.timedelta(days=i)
            until = self.since + datetime.timedelta(days=i+1)
            since = since.strftime('%Y-%m-%d')
            until = until.strftime('%Y-%m-%d')
            query = TwitterSearch.creat_query(self.keyword, since, until, self.lang)
            twsi = TwitterSearch(query, self.max_tweets, since, self.path)
            tp.submit(twsi.spider)
            #twsi.spider()
        tp.shutdown(wait=True)



class TwitterSpyder:
    def __init__(self, keywords, start_y, start_m, start_d, end_y, end_m, end_d, chromedriver_path, write_path):
        '''

        :param keywords:  关键词列表  list 类型
        :param start_y:   开始年份
        :param start_m:   开始月份
        :param start_d:   开始日
        :param end_y:     结束年份
        :param end_m:     结束月
        :param end_d:     结束日
        :param chromedriver_path:  chromedriver安装路径
        '''
        self.start_date = str(start_y)+"-"+ str(start_m)+"-"+str(start_d)
        self.end_date = str(end_y)+"-"+str(end_m)+"-"+str(end_d)
        self.keywords = keywords
        self.path = chromedriver_path
        self.write_path = write_path  # 下载的csv所在目录

    def spy(self):
        days = pd.date_range(self.start_date, self.end_date, freq='6D')
        for keyword in self.keywords:
            for i in range(len(days) - 1):
                begin = str(days[i]).split(" ")[0]
                end = str(days[i + 1]).split(" ")[0]
                select_tweets_since = begin  # "2020-08-01"#input("Enter the start date in (yyyy-mm-dd): ")
                select_tweets_until = end  # "2021-02-01" #input("Enter the end date in (yyyy-mm-dd): ")
                select_tweets_since = datetime.datetime.strptime(
                    select_tweets_since, '%Y-%m-%d')
                select_tweets_until = datetime.datetime.strptime(
                    select_tweets_until, '%Y-%m-%d')
                lang = 1  # int(input("0) All Languages 1) English | 2) Italian | 3) Spanish | 4) French | 5) German | 6) Russian | 7) Chinese\nEnter the language you want to use: "))
                threads = 10
                choose = 1  # int(input(
                # "input what kind of method you want to get:\n1).the day you want get some tweets   2).the day you want get enough tweets :"))'''
                if choose == 1:
                    max_tweets = 110  # int(
                    # input("Enter the maximum tweets number that every day you will collect:"))
                    mul = MultiThread(keyword, select_tweets_since,
                                      select_tweets_until, lang, max_tweets,self.path ,threads)
                    mul.search_thread()
                elif choose == 2:
                    mul = MultiThread(keyword, select_tweets_since,
                                      select_tweets_until, lang, None, self.path,threads)
                    mul.search_thread()
                print("本次获得了{}条数据".format(Tweet.total))
                df.to_csv(self.write_path+"/"+keyword + "_" + begin + "_" + end + ".csv")
                df = df.drop(index=df.index)

        return df



if __name__ == '__main__':
    keywords = ['nuclear wastewater', 'Nuclear pollution', 'Nuclear emissions']
    a =TwitterSpyder(keywords, 2021, 5, 1, 2021, 6, 1, r'F:\Social-Web-Mining\chromedriver.exe', 'Data')
    a.spy()