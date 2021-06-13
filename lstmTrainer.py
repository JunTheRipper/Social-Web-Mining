import math
import pandas as pd
import numpy as np
import numpy
import matplotlib.pyplot as plt
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import os
from sklearn import preprocessing
from keras.models import Sequential, load_model
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler

def create_dataset(dataset, look_back=1):
    '''构建数据集'''
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return numpy.array(dataX), numpy.array(dataY)


class LSTM_data_Analyser():
    def __init__(self, data: pd.DataFrame):
        '''
        :param data: 原始的数据集
        '''
        self.data = data
        self.dataset = None
        self.testX = None
        self.trainX = None
        self.testY = None
        self.trainY = None
        self.scaler = None

    def processing(self):
        '''
        数据预处理
        :return: pd.DataFrame 处理后的相关data数据
        '''
        dataset = self.data.values
        # print(dataset)
        dataset = dataset.astype('float32')
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        dataset = self.scaler.fit_transform(dataset)
        self.dataset = dataset
        return dataset

    def cut_test_train(self):
        '''切割训练集和测试集'''
        numpy.random.seed(7)
        # split into train and test sets
        train_size = int(len(self.dataset) * 0.67)
        test_size = len(self.dataset) - train_size
        train, test = self.dataset[0:train_size, :], self.dataset[train_size:len(self.dataset), :]

        # use this function to prepare the train and test datasets for modeling
        look_back = 1
        self.trainX, self.trainY = create_dataset(train, look_back)
        self.testX, self.testY = create_dataset(test, look_back)

        # reshape input to be [samples, time steps, features]
        self.trainX = numpy.reshape(self.trainX, (self.trainX.shape[0], 1, self.trainX.shape[1]))
        self.testX = numpy.reshape(self.testX, (self.testX.shape[0], 1, self.testX.shape[1]))

    def LSTM_generator(self):
        model = Sequential()
        model.add(LSTM(4, input_shape=(1, 1)))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(self.trainX, self.trainY, epochs=100, batch_size=1, verbose=2)
        # make predictions
        trainPredict = model.predict(self.trainX)
        testPredict = model.predict(self.testX)
        # invert predictions
        trainPredict = self.scaler.inverse_transform(trainPredict)
        self.trainY = self.scaler.inverse_transform([self.trainY])
        testPredict = self.scaler.inverse_transform(testPredict)
        self.testY = self.scaler.inverse_transform([self.testY])

        trainScore = math.sqrt(mean_squared_error(self.trainY[0], trainPredict[:, 0]))
        print('Train Score: %.2f RMSE' % (trainScore))
        testScore = math.sqrt(mean_squared_error(self.testY[0], testPredict[:, 0]))
        print('Test Score: %.2f RMSE' % (testScore))

        trainPredictPlot = numpy.empty_like(self.dataset)
        trainPredictPlot[:, :] = numpy.nan
        trainPredictPlot[self.look_back:len(trainPredict) + self.look_back, :] = trainPredict

        # shift test predictions for plotting
        testPredictPlot = numpy.empty_like(self.dataset)
        testPredictPlot[:, :] = numpy.nan
        testPredictPlot[len(trainPredict) + (self.look_back * 2) + 1:len(self.dataset) - 1, :] = testPredict

        # plot baseline and predictions
        plt.plot(self.scaler.inverse_transform(self.dataset))
        plt.plot(trainPredictPlot)
        plt.plot(testPredictPlot)
        plt.show()


if __name__ == '__main__':
    data = pd.read_csv("确诊-时间.csv", engine='python', skipfooter=3)
    data["日期"] = pd.to_datetime(data["日期"])
    data.index = data["日期"]
    data.drop("Unnamed: 0", axis=1, inplace=True)
    data.drop("日期", axis=1, inplace=True)

    data_any = LSTM_data_Analyser(data)
    data_any.LSTM_generator()
