import pandas as pd


class FileStore:
    def __init__(self, data: pd.DataFrame, name: str):
        '''
        :param data:  预存储数据
        :param name:  存储的csv名称(不用加路径，只写存储名称)
        '''
        self.pdword = data
        self.name = name # 不要加.csv

    def download_as_csv(self, filename: str = None):
        if not filename is None:
            self.pdword.to_csv(filename + self.name+'.csv', index=False)
        else:
            self.pdword.to_csv("results/random-nuclear/Res-Dat/" +
                               self.name+'.csv', index=False)
        print("OK")

    def cmt_download_into_mongo_db(self):
        import pymongo
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client['result-data']
        dbcollection = db[self.name]
        authorList = self.pdword['author'].values
        contentList = self.pdword['content'].values
        timeList = self.pdword['time'].values

        for i in range(len(authorList)):
            jsdata ={
                'author':authorList[i],
                'content':contentList[i],
                'time':timeList[i]
            }
            dbcollection.insert_one(jsdata)

        print("Insert all over!")

    def cmt_download_into_mysql(self, user:str, passwd:str, port:int = 3306):
        import pymysql

        authorList = self.pdword['author'].values
        contentList = self.pdword['content'].values
        timeList = self.pdword['time'].values

        db = pymysql.connect(host='127.0.0.1', user=user, password=passwd,
                             db='resultdata', port=port, charset='utf8')
        conn = db.cursor()  # 获取指针以操作数据库
        conn.execute('set names utf8')

        for i in range(len(authorList)):
            t = [authorList[i], contentList[i], timeList[i]]
            sql = u"INSERT INTO resultdata(author,content,time) VALUES(%s,%s,%s)"

            conn.execute(sql, t)
            db.commit()

        conn.close()
        db.close()


if __name__ == '__main__':
    fileStore = FileStore("helloworld")
    fileStore.download_as_csv()