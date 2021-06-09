# 代码实现太多的数据切割技术
import os
# import pandas as pd
import time
import random

##########删除缺失值、去重##############
'''
data = pd.read_csv("weibo-processed-B.csv",encoding="utf8")
print(data.isnull().sum())
data = data.dropna()
data.reset_index(drop=True,inplace=True)
print(data.isnull().sum())
result = data.drop_duplicates(['微博内容'],keep='last')
result.reset_index(drop=True,inplace=True)
result.to_csv("allData.csv",encoding="utf8",index=False)
'''

def mkSubFile(lines, head, srcName, sub):
    [des_filename, extname] = os.path.splitext(srcName)
    filename = des_filename + '_' + str(sub) + extname
    print('make file: %s' % filename)
    fout = open(filename, 'w',encoding="utf8")
    try:
        fout.writelines([head])
        fout.writelines(lines)
        return sub + 1
    finally:
        fout.close()


def splitByLineCount(filename: str, count: int):
    '''

    :param filename:  写入的目标csv文件
    :param count:
    :return:
    '''
    fin = open(filename, encoding="utf8")
    try:
        head = fin.readline()
        buf = []
        sub = 1
        for line in fin:
            buf.append(line)
            if len(buf) == count:
                sub = mkSubFile(buf, head, filename, sub)
                buf = []
        if len(buf) != 0:
            sub = mkSubFile(buf, head, filename, sub)
    finally:
        fin.close()

def dataRandom(filename: str, writename = None):
    fin = open(filename, encoding="utf8")
    try:
        head = fin.readline()
        lines = fin.readlines()
        random.shuffle(lines)

        if writename == None:
            with open("./results/random-nuclear/allnuclearRandom.csv", 'w', encoding='utf8') as f:
                f.write(head)
                f.writelines(lines)
        else:
            with open(writename, 'w', encoding='utf8') as f:
                f.write(head)
                f.writelines(lines)
    finally:
        fin.close()

if __name__ == '__main__':

    dataRandom("./results/nuclear.csv")
    splitByLineCount('./results/random-nuclear/allnuclearRandom.csv', 2500)#每个小的csv文件存放1000条
