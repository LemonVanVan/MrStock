# encoding:utf-8
from __future__ import division
import redis,time

class hqtest():

    def __init__(self,file_path,start_time,end_time,k_tiem,redis_key,stock_name):
        self.file_path = file_path
        self.start_time = int(start_time) #分K开始时间
        self.end_time = int(end_time) #分K结束时间
        self.redis_key = redis_key
        self.k_tiem = int(k_tiem)
        self.price = []                     #成交价
        self.mvol =[]                       #成交量
        self.price_index = []               #数组中价格对应的角标
        self.mark = 0                       #数组中每个元素的角标，根据角标，方便取出指定分K的开盘价，昨日收盘价，以及计算成交量
        self.time_price=[]                  #当前分时点的价格
        self.stock_name = stock_name

    def run(self):
        r = redis.Redis(host="192.168.10.210",port =6479,db=0)
        sum_row = len(r.zrange(self.redis_key,0,5000))
        f = open(self.file_path,'a')
        f.write("***************************" + self.stock_name + str(self.end_time +1)+ "分K为*****************************" + "\n")
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print u"开始执行：" + str(now_time)
        try:
            for index in range(0,sum_row): #获取redis中指定股票的所有交易明细valu值条数
                hq = r.zrange(self.redis_key,index,index)     #遍历redis中指定股票的所有交易明细valu值
                detail = str(hq[0]).split(',')  #把每一行value值处理为一个数组，方便取出value值中指定的数据
                # print detail
                if (self.end_time >= int(detail[0]) > self.start_time):   #因为不确定当前时间段，在redis中value值是第几行，目前采取遍历所有行；处理所有行中改时间段的分K
                    # print u"开始写入"
                    self.price.append(float(detail[5]))              #把每笔成交价格写入price数组中
                    self.mvol.append(int(detail[6]))              #把每笔成交量写入mvol数组中
                    f.write("交易时间：" +str(detail[0]) + "; 成交价：" + str(detail[5]) +
                            "; 成交量：" + str(detail[6]) + '\n')    #把改分K时间段的数据写入本地
                    self.mark =self.mark +1
                    if (int(detail[0]) >= self.k_tiem):     #分K开始时间
                        # print mark
                        self.price_index.append(self.mark)               #把分K开始时间的角标，存入price_index角标数组中
                        # print price_index
                        # print price
                        self.time_price.append(self.price[self.mark-1])       #把分K第一点开始的价格存入time_price数组中
                        # print time_price

                    # f.write("交易时间：" +str(detail[0]) + ";卖5-" + str(detail[12]) + "；卖4-" + str(detail[14]) +
                    #         ";卖3-" + str(detail[16]) + "；卖2-" + str(detail[18])+
                    #         ";卖1-" + str(detail[20]) + "\n")

            toal_vol=round(float((self.mvol[-1]-self.mvol[self.price_index[0]-2])/100),2)   #计算改分K的总成交量
            zf = round(((self.price[-1]-self.price[self.price_index[0]-2])/self.price[self.price_index[0]-2])*100,2)  #计算改分K的涨幅
            f.write("***************************" + self.stock_name + str(self.end_time +1)+ "分K为*****************************" + "\n")
            f.write("昨日收盘价为：" + str(self.price[self.price_index[0]-2]) + "\n")
            f.write("开盘价为：" + str(self.price[self.price_index[0]-1]) + "\n")
            f.write("最新价为：" + str(self.price[-1]) + "\n")
            f.write("最高价为：" + str(max(self.time_price)) + "\n")
            f.write("最低价为：" + str(min(self.time_price)) + "\n")
            f.write("今日收盘价：" + str(self.price[-1]) + "\n")
            f.write("涨幅为：" +str(zf) + "%" + "\n")
            f.write("成交量为：" + str(toal_vol) + "\n")
        except:
            print u"出错"
            f.close()
            pass
        f.close()
        # print u'写入完成'
        over_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print u"执行结束：" + str(over_time)

if __name__ == "__main__":
    # hqtest()方法需要参数：写入本地文件路径；分K开始时间段，分K结束时间段；分K起始时间，测试股票redis的key值
    hqtest("D:/Desktop/detail.txt",20161116095900,20161116100499,20161116100000,"stocksir:dt:sz002444",'巨星科技').run()

