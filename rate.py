# -*- coding: utf-8 -*-
import requests,os,time

def Get_stock_detail(stock_code,release_time,first_price,second_price,*market_day):
    NPR = []
    times = []
    rate = []
    max_rate = []
    url = "https://mk.api.guxiansheng.cn/quote/?appid=gxs&mod=quote&method=dealinfo_data&fromwhere=cd&finalCode=" + stock_code + \
          "&pageNo=1&pageSize=5000"
    response = requests.get(url)
    detail = response.json()['data']
    # print detail

    now_time = time.strftime('%H:%M', time.localtime(time.time())) #获取当前时间

    if int(market_day[0]) != 0:   #交易日大于0
        if (9 <= int(release_time[:2]) <= 15) and (25 <= int(release_time[3:])):  #股机、锦囊发布时间在盘中
            for index in range(0,len(detail)):
                NPR.append(float(detail[index]['PRI']))
                times.append(str(detail[index]['DATE'][:5]))
            NPR.reverse()
            times.reverse()
            # print times
            # print NPR
            # print times.index(release_time) # 发布时间对应的坐标
            release_price = NPR[times.index(release_time)] #发布时间对应的股票价格
            # print release_price,NPR[0:times.index(release_time)+1]
            print u'股票发布后的最高价为:' + str(max(NPR[times.index(release_time):])) #查询出发布时间后的最高价
            for now_price in NPR[times.index(release_time):]:  #与第一、第二买入价对比，算出当前收益
                if now_price > first_price:
                    rate.append(round(((now_price / release_price)-1)*100,2))
                elif second_price < now_price <= first_price:
                    rate.append(round(((now_price / first_price) - 1) * 100, 2))
                else:
                    rate.append(round(((now_price / second_price) - 1) * 100, 2))
            print u'当前收益为：' + str(rate[-1])
            for index in range(times.index(release_time),len(times)):  #根据发布时间的价格与第一、第二买入价对比，算出最高收益
                if NPR[index] > first_price:
                    max_rate.append(round(((NPR[index] / release_price) -1)*100,2))
                elif second_price < NPR[index] <= first_price:
                    max_rate.append(round(((NPR[index] / first_price) - 1) * 100, 2))
                else:
                    max_rate.append(round(((NPR[index] / second_price) - 1) * 100, 2))
            print u'最大收益为：' + str(max(max_rate))
        else: #股机、锦囊发布时间非盘中
            if len(detail) <= 0:
                print u'还未开盘'
            else:
                for index in range(0, len(detail)):
                    NPR.append(float(detail[index]['PRI']))
                    times.append(str(detail[index]['DATE'][:5]))
                NPR.reverse()
                times.reverse()
                release_price = NPR[0]  # 发布时间对应的股票价格
                print u'股票发布后的最高价为:' + str(max(NPR))  # 查询出发布时间后的最高价
                for now_price in NPR[0:]:  # 与第一、第二买入价对比，算出当前收益
                    if now_price > first_price:
                        rate.append(round(((now_price / release_price) - 1) * 100, 2))
                    elif second_price < now_price <= first_price:
                        rate.append(round(((now_price / first_price) - 1) * 100, 2))
                    else:
                        rate.append(round(((now_price / second_price) - 1) * 100, 2))
                print u'当前收益为：' + str(rate[-1])
                for index in range(times.index(release_time), len(times)):  # 根据发布时间的价格与第一、第二买入价对比，算出最高收益
                    if NPR[index] > first_price:
                        max_rate.append(round(((max(NPR[index:]) / release_price) - 1) * 100, 2))
                    elif second_price < NPR[index] <= first_price:
                        max_rate.append(round(((max(NPR[index:]) / first_price) - 1) * 100, 2))
                    else:
                        max_rate.append(round(((max(NPR[index:]) / second_price) - 1) * 100, 2))
                print u'最大收益为：' + str(max(max_rate))

            if (9 <= int(now_time[:2])) and (1 <= int(now_time[3:])):
                f = open("E:/plan_jn_test/rate.txt", 'rb')
                history_rate = f.readlines()
                if float(history_rate[0]) <= max(max_rate):
                    f = open("E:/plan_jn_test/rate.txt",'w')
                    f.write(str(max(max_rate)) + '\n')
            f.close()

    else:   #交易日=0
        if (9 <=int(release_time[:2]) <= 15):  #股机、锦囊发布时间在盘中
            for index in range(0,len(detail)):
                NPR.append(float(detail[index]['PRI']))
                times.append(str(detail[index]['DATE'][:5]))
            NPR.reverse()
            times.reverse()
            # print times
            # print NPR
            # print times.index(release_time) # 发布时间对应的坐标
            release_price = NPR[times.index(release_time)] #发布时间对应的股票价格
            # print release_price,NPR[0:times.index(release_time)+1]
            print u'股票发布后的最高价为:' + str(max(NPR[times.index(release_time):])) #查询出发布时间后的最高价
            for now_price in NPR[times.index(release_time):]:  #与第一、第二买入价对比，算出当前收益
                if now_price > first_price:
                    rate.append(round(((now_price / release_price)-1)*100,2))
                elif second_price < now_price <= first_price:
                    rate.append(round(((now_price / first_price) - 1) * 100, 2))
                else:
                    rate.append(round(((now_price / second_price) - 1) * 100, 2))
            print u'当前收益为：' + str(rate[-1]) + "%"

            for index in range(times.index(release_time),len(times)):  #根据发布时间的价格与第一、第二买入价对比，算出最高收益
                if NPR[index] > first_price:
                    max_rate.append(round(((max(NPR[index:]) / release_price) -1)*100,2))
                elif second_price < NPR[index] <= first_price:
                    max_rate.append(round(((max(NPR[index:]) / first_price) - 1) * 100, 2))
                else:
                    max_rate.append(round(((max(NPR[index:]) / second_price) - 1) * 100, 2))
            print u'最大收益为：' + str(max(max_rate)) + "%"

        else: #股机、锦囊发布时间非盘中
            if len(detail) <= 0:
                print u'还未开盘'
            else:
                for index in range(0, len(detail)):
                    NPR.append(float(detail[index]['PRI']))
                    times.append(str(detail[index]['DATE'][:5]))
                NPR.reverse()
                times.reverse()
                release_price = NPR[0]  # 发布时间对应的股票价格
                print u'股票发布后的最高价为:' + str(max(NPR))  # 查询出发布时间后的最高价
                for now_price in NPR[0:]:  # 与第一、第二买入价对比，算出当前收益
                    if now_price > first_price:
                        rate.append(round(((now_price / release_price) - 1) * 100, 2))
                    elif second_price < now_price <= first_price:
                        rate.append(round(((now_price / first_price) - 1) * 100, 2))
                    else:
                        rate.append(round(((now_price / second_price) - 1) * 100, 2))
                print u'当前收益为：' + str(rate[-1]) + "%"
                for index in range(0, len(times)):  # 根据发布时间的价格与第一、第二买入价对比，算出最高收益
                    if NPR[index] > first_price:
                        max_rate.append(round(((NPR[index] / release_price) - 1) * 100, 2))
                    elif second_price < NPR[index] <= first_price:
                        max_rate.append(round(((NPR[index] / first_price) - 1) * 100, 2))
                    else:
                        max_rate.append(round(((NPR[index] / second_price) - 1) * 100, 2))
                print u'最大收益为：' + str(max(max_rate)) + "%"
            if (9 <= int(now_time[:2])) and (1 <= int(now_time[3:])):
                f1 = open("E:/plan_jn_test/rate.txt", 'rb')
                f2 = open("E:/plan_jn_test/marke_price.txt", 'w')
                history_rate = f1.readlines()
                if float(history_rate[0]) <= max(max_rate):
                    f = open("E:/plan_jn_test/rate.txt",'w')
                    f.write(str(max(max_rate)) + '\n')
                # f.write(stock_code + "在" + time.strftime('%m:%d', time.localtime(time.time())) +"的最高收益为：" + str(max(max_rate)) + '\n')
                if (9 <= int(release_time[:2]) <= 15) and (25 <= int(release_time[3:])):
                    NPR[times.index(release_time)]
            f1.close()

if __name__ == "__main__":
    Get_stock_detail('sh600249','10:21',11.91,11.37,0)  #传入股票代码、发布时间、第一价格、第二价格,第N个交易日
    # os.system("pause")




