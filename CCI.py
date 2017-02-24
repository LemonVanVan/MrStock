# -*- coding: utf-8 -*-
"""
TYP:=(HIGH+LOW+CLOSE)/3;
       CCI:(TYP-MA(TYP,N))/(0.015*AVEDEV(TYP,N));
TYP比较容易理解，（最高价+最低价+收盘价）÷3
MA(TYP,N) 也比较简单，就是N天的TYP的平均值
AVEDEV(TYP,N) 比较难理解，是对TYP进行绝对平均偏差的计算。
也就是说N天的TYP减去MA(TYP,N)的绝对值的和的平均值。
表达式：
MA = MA(TYP,N)
AVEDEV(TYP,N) =( | 第N天的TYP - MA |   +  | 第N-1天的TYP - MA | + ...... + | 第1天的TYP - MA | ) ÷ N
CCI = （TYP－MA）÷ AVEDEV(TYP,N)   ÷0.015
"""

import requests,os

def Get_stock_detail(stock_code):
    times=[]    #日期
    close=[]  #收盘价
    hpri = [] #最高价
    lpri = [] #最低价
    url = "http://mk.api.guxiansheng.cn/quote/?mod=quote&method=kline_data&begindate=&" \
          "finalCode=" + stock_code + "&fqtype=&num=200&type=day&appid=gxs"   #参数中num为获取日K的点数，200为200个日期点
    r = requests.get(url)
    all_time = r.json()['data']['timeZ']     #获取日K的所有日期
    all_data = r.json()['data']['datas']   #获取日K中所有日期的数据明细

    for time in all_time:   #交易时间
        times.append(time)

    for npri in all_data:   #当日收盘价
        close.append(npri['NPRI'])

    for today_hpri in all_data:   #当日最高价
        hpri.append(today_hpri['HPRI'])

    for today_lpri in all_data:   #当日最低价
        lpri.append(today_lpri['LPRI'])
    TYP = []
    for i in range(0,len(close)):  #根据最高价、最低、收盘价 算出中价
        typ_value = (close[i] + hpri[i] + lpri[i])/3
        TYP.append(typ_value)

    MA  = []
    N = 14
    for j in range(0,len(TYP)):  #计算中间中价14天的MA值
        ma_value = sum(TYP[j:N])/14
        MA.append(ma_value)
        N = N + 1
        if N == len(TYP)+1:
            break

    AVEDEV = []
    for x in range(0,len(MA)):  #计算收盘价、最高价、最低价对应的中价的绝对平均偏差
        avedev_sum = 0
        for y in range(0,14):
            abs_sum = abs(TYP[x+y]-MA[x])
            avedev_sum = avedev_sum + abs_sum
        avedev_sum = avedev_sum/14
        AVEDEV.append(avedev_sum)

    CCI = []
    for index in range(0,len(MA)): #计算CCI
        value = round((TYP[index]- MA[index])/(AVEDEV[index]*0.015),2)
        CCI.append(value)

    for i in range(0,len(CCI)): #输出对应日期的CCI
        print str(times[i]) + u"的CCI值为：" + str(CCI[i])

if __name__ == "__main__":
    Get_stock_detail("sh603868") #传入股票代码，加前缀
    os.system("pause")













