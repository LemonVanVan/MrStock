# -*- coding: utf-8 -*-
"""
MTM（动量线指标）
计算方法：
MTM（N日）=C-CN       C=当日收盘价    CN=N日前的收盘价  N默认值12
MAMTM =MTM/M      求MTM的M日平滑数据    M默认值6
"""

import requests,os

def Get_stock_detail(stock_code):
    times=[]    #日期
    close=[]  #收盘价
    MTM = [] #MTM
    MAMTM = []
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
    N = 13
    mtm_index = 0
    while True:
        mtm_value = round((close[N-1] -close[mtm_index]),2)
        N = N + 1
        mtm_index = mtm_index +1
        MTM.append(mtm_value)
        if N == len(close)+1:
            break
    MTM.reverse()
    M = 6

    for mamtm_index in range(0,len(MTM)):
        mamtm_value = round((sum(MTM[mamtm_index:M])/6),2)
        M = M+1
        MAMTM.append(mamtm_value)
        if M == len(MTM)+1:
            break

    for i in range(0,len(MAMTM)):
        print str(times[i]) + u"的MTM值为：" + str(MTM[i]) + u";MAMTM值为：" + str(MAMTM[i])

if __name__ == "__main__":
    Get_stock_detail("sh603868") #传入股票代码，加前缀
    os.system("pause")












