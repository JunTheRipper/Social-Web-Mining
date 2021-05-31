# 项目内容： 尝试爬取twitter社交平台的数据
# 调用gitHub上的相关项目实现
from twitter_scraper import get_tweets

def spy(m):
    for i in get_tweets('#nuclearwater', pages=m):
        print(i['username'], i['text'],i['time'])

while True:
    try:
        spy(5)
    except Exception as e:
        print(e)
        # spy(5)