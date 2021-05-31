# 丁香园类数据集分类分析库
# 包括相关的数据变化趋势显示和变化和分类算法设计和实现分析
import pandas as pd
import matplotlib.pyplot as plt


class Analyser:
    def __init__(self, D_data):
        self.D_data = D_data
        #训练集、测试集初始化
        self.train_X = None
        self.train_Y = None
        self.test_X = None
        self.test_Y = None


    def show_raw_hist(self, key, value, title, savepath=None):
        '''

        :param key: 作图的键,x轴
        :param value: 作图的值， y轴
        :param title:
        :return: picture of data
        '''
        plt.plot(self.D_data[key], self.D_data[value])
        plt.xlabel(key)
        plt.ylabel(value)
        plt.title(title)

        if savepath == None:
            plt.show()
        else:
            plt.savefig(savepath, dpi=600)

    def show_otherPic(self, title, lister=None,  savepath=None ):
        '''根据label制作其他图表（自己设计吧）'''


        plt.title(title)
        if savepath == None:
            plt.show()
        else:
            plt.savefig(savepath, dpi=600)
        pass

    # add other related pictures



    # add other pictures
    def n_cut_data(self):
        '''
        切割数据集为测试集和训练集
        :return:
        '''
        pass

    def n_classify_knn(self, label='label'):
        '''

        :param label:  分类的参考依据
        :return:
        '''
        pass

    def n_classify_decisiontree(self, label='label'):
        '''
        决策树分类
        :param label:  分类的参考依据
        :return:
        '''
        pass

    def n_classify_guassbayes(self, label='label'):
        '''
        高斯贝叶斯分类器
        :param label:  分类的参考依据
        :return:
        '''
        pass

    def n_classify_svm(self, label='label'):
        '''
        支持向量机分类器
        :param label:  分类的参考依据
        :return:
        '''
        pass

    def n_classify_randomforest(self, label='label'):
        '''
        随机森林分类器
        :param label:  分类的参考依据
        :return:
        '''
        pass



