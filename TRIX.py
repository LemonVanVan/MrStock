# -*- coding: utf-8 -*-
"""
TRIX（三重指数平滑平均线）
计算方法：
1. X=ema(close,N)，首先计算收盘价的N日移动平均值，
2.对X作N日平滑处理，得出Y值，即Y=ema(X,N),
3.对Y再次N日平滑处理，得出TR值，即TR=ema(Y,N)
以上三个步骤的意思是，对N日收盘均价作3次平滑处理后，得出最终值TR
4.求TRIX值
  TRIX=【（TR-上一日TR）/上一日TR】*100
5.求TRIX值的M日简单移动平均值 MATRIX
  MATRIX=MA(TRIX,M)
使用方法：
TRIX从下上穿MATRIX，设置金叉符号，红色上箭头
TRIX从上下穿MATRIX，设置死叉符号，蓝色下箭头
"""
import requests,os

def data_replace(data):  #截取小数点后两位
    data = str(data)
    index = data.index('.')
    return float(data[:index+3])

def Get_stock_detail(stock_code):
    times=[]    #日期
    close=[]  #收盘价

    url = "http://mk.api.guxiansheng.cn/quote/?mod=quote&method=kline_data&begindate=&" \
          "finalCode=" + stock_code + "&fqtype=&num=200&type=day&appid=gxs"   #参数中num为获取日K的点数，200为200个日期点
    r = requests.get(url)
    all_time = r.json()['data']['timeZ']     #获取日K的所有日期
    all_data = r.json()['data']['datas']   #获取日K中所有日期的数据明细

    for time in all_time:   #交易时间
        times.append(time)

    for npri in all_data:   #当日收盘价
        close.append(npri['NPRI'])
    close.reverse()
    N= 12
    X = []
    Y = []
    Z = []
    i = close[0]

    for x_index in range(0,len(close)):  #用收盘价计算第一次EMA
        EMA_X = round(((2 * close[x_index]) + ((N-1) * i))/(N + 1),3)
        X.append(EMA_X)
        i = X[x_index]

    j = X[0]
    for y_index in range(0,len(X)):  #用收盘价计算后的EMA再次计算EMA
        EMA_Y = round(((2 * X[y_index]) + ((N-1) * j))/(N + 1),3)
        Y.append(EMA_Y)
        j = Y[y_index]

    q = Y[0]
    for Z_index in range(0,len(Y)): #第三次计算EMA
        EMA_Z = round(((2 * Y[Z_index]) + ((N-1) * q))/(N + 1),3)
        Z.append(EMA_Z)
        q = Z[Z_index]

    TRIX = []
    for TRIX_index in range(1,len(Z)):  #计算TRIX值
        value = round(((Z[TRIX_index]-Z[TRIX_index-1])/Z[TRIX_index-1])*100,3)
        TRIX.append(value)

    MATRIX = []
    M = 20
    for MATRIX_index in range(0,len(TRIX)): #计算MATRIX值
        MATRIX_value = round(sum(TRIX[MATRIX_index:M])/20,3)
        M = M+1
        MATRIX.append(MATRIX_value)
        if M == len(TRIX)+1:
            break


    TRIX.reverse()
    MATRIX.reverse()
    for i in range(0,len(MATRIX)): #输出对应日期的TRIX和MATRIX
        print str(times[i]) + u"的TRIX值为：" + str(TRIX[i]) + u";MATRIX值为：" + str(MATRIX[i])

if __name__ == "__main__":
    Get_stock_detail("sh603868") #传入股票代码，加前缀
    os.system("pause")













