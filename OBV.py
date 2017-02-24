# -*- coding: utf-8 -*-
"""
OBV计算方法：
主公式：当日OBV=前一日OBV+今日成交量
1.基期OBV值为0，即该股上市的第一天，OBV值为0
2.若当日收盘价＞上日收盘价，则当日OBV=前一日OBV＋今日成交量
3.若当日收盘价＜上日收盘价，则当日OBV=前一日OBV－今日成交量
4.若当日收盘价＝上日收盘价，则当日OBV=前一日OBV
"""

import requests,os

def Get_stock_detail(stock_code):
    times=[]    #日期
    close=[]  #收盘价
    tvols = [] #成交量
    url = "http://mk.api.guxiansheng.cn/quote/?mod=quote&method=kline_data&begindate=&" \
          "finalCode=" + stock_code + "&fqtype=&num=200&type=day&appid=gxs"   #参数中num为获取日K的点数，200为200个日期点
    r = requests.get(url)
    all_time = r.json()['data']['timeZ']     #获取日K的所有日期
    all_data = r.json()['data']['datas']   #获取日K中所有日期的数据明细

    for time in all_time:   #交易时间
        times.append(time)
    times.reverse()

    for npri in all_data:   #当日收盘价
        close.append(npri['NPRI'])
    close.reverse()

    for tovl in all_data:   #当日成交量
        tvols.append(round(tovl['TVOL']/100,0))
    tvols.reverse()

    base_obv = 0
    obv = []
    obv.append(base_obv)
    for i in range(0,len(times)-1):  #通过收盘价比较计算当日OBV
        if close[i+1] > close[i]:
            today_obv = base_obv + tvols[i+1]
            obv.append(today_obv/100)
        elif close[i+1] < close[i]:
            today_obv = base_obv - tvols[i+1]
            obv.append(today_obv/100)
        else:
            today_obv = base_obv
            obv.append(today_obv/100)
        base_obv =today_obv
    for i in range(0,len(obv)):
        print str(times[i]) + u"的OBV值为：" + str(obv[i])

if __name__ == "__main__":
    Get_stock_detail("sh603868") #传入股票代码，加前缀
    os.system("pause")












