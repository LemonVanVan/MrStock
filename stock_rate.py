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
    release_price = []     #股票当天的价格
    release_PriceRange = []   #股票发布时的价格区间（快照一分钟内的价格）
    #stock_price = [] #股票发布后的价格
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
                               #index() 方法检测字符串minute_time中是否包含子字符串release_time;返回开始的索引值
                               #max() 方法返回其参数最大值
    stock_price = (NPR[0:minute_time.index(release_time)])     #股票发布后的价格区间
    stock_price.reverse()      #用于反向列表中元素
    # print stock_price
    for price in release_price:
        print price
        for now_price in stock_price:  #与第一、第二买入价对比，算出当前收益
            print now_price

            if now_price > first_price:       #股机非交易时间发布，开盘后价格没有触及推荐买入价，当前收益=当前价/开盘价-1
                                              #股机交易时间发布，发布后价格没有触及推荐买入价，当前收益=当前价/发出时价格-1
                rate.append(round(((now_price / price)-1)*100,2))   #round()返回小数点四舍五入到2个数字。

            elif second_price < now_price <= first_price:   #股机非交易时间发布，开盘后价格触及第一推荐买入价后,当前收益=当前价/第一推荐买入价-1
                                                            #股机交易时间发布，发布后价格触及第一推荐买入价后,当前收益=当前价/第一推荐买入价-1
                rate.append(round(((now_price / first_price) - 1) * 100, 2))

            else:         #股机非交易时间发布，开盘后价格触及第二推荐买入价后,当前收益=当前价/第二推荐买入价-1
                          #股机交易时间发布，发布后价格触及第二推荐买入价后,当前收益=当前价/第二推荐买入价-1
                rate.append(round(((now_price / second_price) - 1) * 100, 2))

        now_rate.append(rate[-1])
        # print u'当前收益计算价格当前价为：' + str(now_price) + u" ;当前收益为"+  str(rate[-1])
    print now_rate
    for price in release_price:

        for index in range(0,minute_time.index(release_time)):  #与第一、第二买入价对比，算出最高收益
            if NPR[minute_time.index(release_time) - index] > first_price:          #股机非交易时间发布，开盘后价格没有触及推荐买入价，最高收益=取所有当前收益的最高值
                                                                                    #股机交易时间发布，发布后价格没有触及推荐买入价，最高收益=取所有当前收益的最高值
                max_rate.append(round(((max(NPR[0:(minute_time.index(release_time) - index)]) / price) -1)*100,2))

            elif second_price < NPR[minute_time.index(release_time) - index] <= first_price:   #股机非交易时间发布，开盘后价格触及第一推荐买入价后,最高收益=取所有当前收益的最高值（包含触及第一买入价之前的当前收益）
                                                                                               #股机交易时间发布，发布后价格触及第一推荐买入价后,最高收益=取所有当前收益的最高值（包含触及第一买入价之前的当前收益）
                max_rate.append(round(((max(NPR[0:(minute_time.index(release_time) - index)]) / first_price) - 1) * 100, 2))

            else:         #股机非交易时间发布，开盘后价格触及第二推荐买入价后,最高收益=取所有当前收益的最大值（包含触及第二买入价之前的当前收益）
                          #股机交易时间发布，发布后价格触及第二推荐买入价后,最高收益=取所有当前收益的最高值（包含触及第二买入价之前的当前收益）
                max_rate.append(round(((max(NPR[0:(minute_time.index(release_time) - index)]) / second_price) - 1) * 100, 2))
        true_MaxRate.append(max(max_rate))
    print true_MaxRate
        # print u'最大收益为：' + str(max(max_rate))

if __name__ == "__main__":
    Get_stock_detail('sz002023','10:35',15,16)  #传入股票代码、发布时间、第一价格、第二价格
    # os.system("pause")
