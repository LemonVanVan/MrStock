# -*- coding: utf-8 -*-

"""
BOLL（布林带）
计算方法：
1、计算中轨
MB=(当前k线收盘价+前k线收盘价+...+前N-1根k线收盘价)/N   N默认为20
2、计算标准差
先计算N根K线差额的平方和
sum=(当前K线收盘价-当前k线MB)^2+(前K线收盘价-前k线MB)^2+...+(第N根K线收盘价-第N根k线MB)^2
再计算标准差(Sqrt表示开方，计算平方根)
MD=K*Sqrt(sum/N)     K为标准差值，默认值为2；N默认为20
3、计算上轨、下轨
UP=MB+MD    （上轨值计算）
DN=MB-MD    （下轨值计算）
"""

import requests,math,os

def Get_close_allday(stock_code):
    allday=[]    #日期
    close=[]  #收盘价数组
    url = 'http://mk.api.guxiansheng.cn/quote/?mod=quote&' \
          'method=kline_data&begindate=&' \
          'finalCode=' + stock_code + '&fqtype=&num=200&' \
          'type=day&appid=gxs'   #参数中num为获取日K的点数，200为200个日期点
    r = requests.get(url)
    dates = r.json()['data']['timeZ']     #获取日K的所有日期
    datasdetail = r.json()['data']['datas']   #获取日K中有点的数据明细

    for datadetail in datasdetail:
        close.append(round((datadetail["NPRI"]),2))      #循环遍历，把明细中的收盘价存在Close数组中

    for data in dates:
        allday.append(int(data.replace('-','')))      #循环遍历，把交易日期存在allday数组中
    # print close[-20:]
    return close,allday

def Get_Boll(close,allday):
    L = len(close)             #计算收盘价数组长度，用于处理MID20的值
    N=20                       #默认N值为0
    start = 0                  #数组分割，起始分割索引为：0
    end = 20                   #数组分割，结束索引为：20 与N值相同

    while True:                    #循环遍历：遍历指定日K长度，用于计算每个日期的MID值
        for price in range(0,len(close)):
            sum_close = 0
            # print start,end,price
            MID=round(sum(close[start:end])/N,2)   #MB的计算公式：计算方法为收盘价数组中，最后一个点的收盘价加前19个点的
                                                  #收盘价只和，再除以20；每循环一次：最后一个点位移一个点
            for i in range(0,20):
                # print close[price+i]
                sum_close= sum_close + round(abs((close[price+i]-MID)**2),2)
            UPPER = MID + 2 * round(math.sqrt(sum_close/20),2)
            LOWER = MID - (UPPER-MID)

            f.write('日期：' + str(allday[price]) + '的MID值为：' + str(MID) +
                    ';UPPER值为：'  + str(UPPER) +
                    ';LOWER值为：' + str(LOWER) + "\n") #计算结果写入：本地文档
            print  (u'日期：' + str(allday[price]) +
                    u'的MID值为：' + str(MID) +
                    u';UPPER值为：'  + str(UPPER) +
                    u';LOWER值为：' + str(LOWER))
            start = start + 1
            end = end + 1
            L = L-1
            if L - N == -1:   #改判断用于判断不足20个点，无法计算时，退出for循环
                f.close()
                break
        break    #for循环结束后，退出while循环

if __name__ == "__main__":

    f = open("D:/Desktop/detail.txt",'w')    #文件写入路径
    close,allday = Get_close_allday('sz002023')
    Get_Boll(close,allday)
    os.system("pause")
    # Get_Upper(MID,close)










