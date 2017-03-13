# -*- coding: utf-8 -*-
import requests,os,time

def Get_stock_detail(stock_code,release_time,first_price,second_price):
    NPR = []
    second_time = []
    minute_time = []
    rate = []
    now_rate = []
    max_rate = []
    true_MaxRate = []
    release_price = []
    release_PriceRange = []
    url = "https://mk.api.guxiansheng.cn/quote/?appid=gxs&mod=quote&method=dealinfo_data&fromwhere=cd&finalCode=" + stock_code + \
          "&pageNo=1&pageSize=5000"
    response = requests.get(url)
    detail = response.json()['data']   #response.json()返回的是一个字典类型的数据，['data']就是从字典里面取键值为data的值
    for index in range(0,len(detail)):
        NPR.append(float(detail[index]['PRI']))
        second_time.append(str(detail[index]['DATE'][:8]))
        minute_time.append(str(detail[index]['DATE'][:5]))
    # print times
    # print NPR
    for i in range(len(second_time)):
        if second_time[i][:5] == release_time:
            release_price.append(NPR[i])
            release_PriceRange.append(str(second_time[i]) +" "+ str(NPR[i]))
            # print str(second_time[i]) +" "+ str(NPR[i])
    print release_PriceRange    ##发布时间对应的股票价格区间
    # print release_price #发布时间对应的股票价格区间
    # print minute_time.index(release_time) # 发布时间对应的坐标
    print u'股票发布后的最高价为:' + str(max(NPR[0:minute_time.index(release_time)])) #查询出发布时间后的最高价
    stock_price = (NPR[0:minute_time.index(release_time)])     #股票发布后的价格区间
    stock_price.reverse()
    # print stock_price
    for price in release_price:
        for now_price in stock_price:  #与第一、第二买入价对比，算出当前收益
            if now_price > first_price:
                rate.append(round(((now_price / price)-1)*100,2))
            elif second_price < now_price <= first_price:
                rate.append(round(((now_price / first_price) - 1) * 100, 2))
            else:
                rate.append(round(((now_price / second_price) - 1) * 100, 2))
        now_rate.append(rate[-1])
        # print u'当前收益计算价格当前价为：' + str(now_price) + u" ;当前收益为"+  str(rate[-1])
    print now_rate
    for price in release_price:

        for index in range(0,minute_time.index(release_time)):  #与第一、第二买入价对比，算出最高收益
            if NPR[minute_time.index(release_time) - index] > first_price:
                max_rate.append(round(((max(NPR[0:(minute_time.index(release_time) - index)]) / price) -1)*100,2))
            elif second_price < NPR[minute_time.index(release_time) - index] <= first_price:
                max_rate.append(round(((max(NPR[0:(minute_time.index(release_time) - index)]) / first_price) - 1) * 100, 2))
            else:
                max_rate.append(round(((max(NPR[0:(minute_time.index(release_time) - index)]) / second_price) - 1) * 100, 2))
        true_MaxRate.append(max(max_rate))
    print true_MaxRate
        # print u'最大收益为：' + str(max(max_rate))

if __name__ == "__main__":
    Get_stock_detail('sz000519','09:48',16.39,16.36)  #传入股票代码、发布时间、第一价格、第二价格
    # os.system("pause")




