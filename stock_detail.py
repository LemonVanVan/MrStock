# -*- coding: utf-8 -*-

import requests,time,pymssql,os

def data_replace(data):  #截取小数点后两位
    data = str(data)
    index = data.index('.')
    return data[:index+3]

def get_one_value(sql):   #获取唯一值
    try:
        conn = pymssql.connect(host = 'xxxxx',user = 'xxxxx',password = 'gxxxxx',
                               database = 'xxxxxx')     #行情数据库连接地址
        cur = conn.cursor()    # 使用cursor()方法获取操作游标
        cur.execute(sql)     # 使用execute方法执行SQL语句
        rows = cur.fetchall()     #获取所有记录列表    #使用 fetchone() 方法是获取单条数据,
        conn.close()      # 关闭数据库连接
        for value in rows:
            return float(value[0])
    except:
        print u"数据库连接失败"


def get_today_money_flow(sql):   #获取今日资金流向
    try:
        conn = pymssql.connect(host = 'xxxxx',user = 'xxxxx',password = 'gxxxxx',
                               database = 'xxxxxx')   #行情数据库连接地址
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        for value in rows:
            return value
    except:
        print u"数据库连接失败"


def get_values(sql): #获取多个值
    try:
        conn = pymssql.connect(host = 'xxxxx',user = 'xxxxx',password = 'gxxxxx',
                               database = 'xxxxxx')   #行情数据库连接地址
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        day_value=[]
        for value in rows:
            day_value.append(float(value[0]))
        return day_value
    except:
        print u"数据库连接失败"


def get_zf(day,stock_code):  #根据天数获取振幅
    close = get_values("select top 10 TCLOSE from dbo.STK_MKT  where seccode = " + stock_code[2:] + " order by SEQ DESC")
    hour_time = int(time.strftime('%H',time.localtime(time.time())))   #time.time()用于获取当前时间戳，localtime()从返回浮点数的时间辍方式向时间元组转换，strftime()格式化日期
    minute_time = int(time.strftime('%M',time.localtime(time.time())))  #time.time()用于获取当前时间戳，localtime()从返回浮点数的时间辍方式向时间元组转换，strftime()格式化日期
    if hour_time >= 15 and minute_time>31:
        return close[day-1]
    else:
        return close[day-1]

def get_tvolume(stock_code):  #获取成交量
    hour_time = int(time.strftime('%H',time.localtime(time.time())))
    minute_time = int(time.strftime('%M',time.localtime(time.time())))
    if hour_time >= 15 and minute_time>8:
        TVOLUME = get_values("select  TOP 6 TVOLUME  from dbo.STK_MKT  where seccode = " + str(stock_code[2:]) + " order by SEQ DESC")
        return (sum(TVOLUME[1:]) /1200)/100
    else:
        TVOLUME = get_values("select  TOP 5 TVOLUME  from dbo.STK_MKT  where seccode = " + str(stock_code[2:]) + " order by SEQ DESC")
        return (sum(TVOLUME) /1200)/100

def unit_replace(value):  #单位替换
    if value >0:
        value = str(value)
        if 9>len(value[:value.index('.')])>=5:
            value = str(float(value[:value.index('.')])/10000)
            index = value.index('.')
            value = value[:index +3] + u'万'   #以万为单位
            return value
        elif len(value[:value.index('.')])>=9:
            value = str(float(value[:value.index('.')])/100000000)
            index = value.index('.')
            value = value[:index +3] + u'亿'   #亿为单位
            return value
        else:
            return value #普通单位
    else:
        value = str(value)
        if 10>len(value[:value.index('.')])>=6:
            value = str(float(value[:value.index('.')])/10000)
            index = value.index('.')
            value = value[:index +3] + u'万'   #以万为单位
            return value
        elif len(value[:value.index('.')])>=10:
            value = str(float(value[:value.index('.')])/100000000)
            index = value.index('.')
            value = value[:index +3] + u'亿'   #亿为单位
            return value
        else:
            return value #普通单位

def Get_stock_detail(stock_code):
    url ="http://mk.api.guxiansheng.cn/quote/?mod=quote&method=time_data&finalCode=" + stock_code +\
         "&fromwhere=cd&num=241&timePoint=0&type=00&appid=gxs&device=36C0FF7E0B81B4C6722D5AA64F3FDD22&token=36C0FF7E0B81B4C6722D5AA64F3FDD22"
    r = requests.get(url)        #发送请求
    NPRI = float(str((r.json()['NPRI'])[:5])) #最新价
    print u'最新价为：' + str(NPRI)
    OPRI = float(str((r.json()['OPRI'])[:5])) #今开
    print u'今开为：' + str(OPRI)
    PPRI =  float(str((r.json()['PPRI'])[:5] ))  #昨收
    print u'昨收为：' + str(PPRI)
    Limit_Up  = data_replace((PPRI + PPRI * 0.1))     #涨停
    print u'涨停为：' + str(Limit_Up)
    Limit_Down = data_replace((PPRI - PPRI * 0.1))     #跌停
    print u'跌停为：' + str(Limit_Down)
    HPRI = float(str((r.json()['HPRI'])[:5])) #最高
    print u'最高为：' + str(HPRI)
    LPRI = float(str((r.json()['LPRI'])[:5])) #最低
    print u'最低为：' + str(LPRI)
    SSCJL = str(float(r.json()['data'][-1]['TVOL'])/100) #成交量
    print u'成交量为：' + unit_replace(SSCJL)
    SSCJE = str(float(r.json()['data'][-1]['TVAL']))  #成交额
    print u'成交额为：' + unit_replace(SSCJE)  #调用自定义的unit_replace函数

    HSL = str(round(((float(SSCJL)*100) /get_one_value("select top 1 FL_SHR from dbo.STK_SHR_STRU where A_STOCKCODE  = " + repr(stock_code[2:]) + "  order by SEQ desc"))*100,2)) + '%' #个股换手率 = （买卖单成交量总和） / 流通股本
    print u'换手率为：' + HSL
    #AVPRI = data_replace(float(r.json()['data'][-1]['TVAL']) /float(r.json()['data'][-1]['TVOL'])) #均价
    #print u'均价为：' + AVPRI
    ZF = data_replace(((HPRI - LPRI)/PPRI ) * 100) + '%'  #振幅
    print u'振幅为：' + ZF
    SYL = data_replace((NPRI / get_one_value("select top 1 EPSP from  dbo.ANA_STK_FIN_IDX where A_STOCKCODE = " + repr(stock_code[2:]) + "  order by SEQ desc")))    #个股市盈率=每股市价/每股税后利润
    print u'市盈率为：' + SYL
    Five_ZF = data_replace((NPRI - get_zf(5,stock_code))/ get_zf(5,stock_code)*100) + "%"     # 板块N日涨幅 = （当前实时指数 - 第N-1日指数） / 第N-1日指数 * 100%）
    print u'5日涨幅为：' + Five_ZF
    Eight_ZF = data_replace((NPRI - get_zf(8,stock_code))/ get_zf(8,stock_code)*100) + "%"     #8日涨幅
    print u'8日涨幅为：' + Eight_ZF
    MGSY = round(get_one_value("select  top 1 EPSP from  ANA_STK_FIN_IDX where A_STOCKCODE = " + repr(stock_code[2:]) + " and RPT_YEAR ='2016' order by SEQ desc"),2)  #每股收益EPSP
    print u'每股收益为：' + str(MGSY)
    MGJZC = data_replace(get_one_value("select  top 1 BPS from  ANA_STK_FIN_IDX where A_STOCKCODE = " + repr(stock_code[2:]) + " and RPT_YEAR ='2016' order by SEQ desc"))  #每股净资产BPS
    print u'每股净资产为：' + MGJZC
    SJL = data_replace(NPRI/float(MGJZC))  #市净率= 每股市价 / 每股净资产  26492.26400004
    print u'市净率为：' + SJL
    open_time = int(len(r.json()['data']))
    LB = data_replace(float(SSCJL)/(get_tvolume(stock_code)*(open_time-1)))  #量比 = 现成交总手/（过去5日平均每分钟成交量×当日累计开市时间（分））
    # print SSCJL,get_tvolume(stock_code),open_time
    print u'量比为：' + LB

    GB = get_one_value(" select top 1 FL_SHR from dbo.STK_SHR_STRU where A_STOCKCODE =" + repr(stock_code[2:]) + "  order by SEQ  desc ")
    LTSZ =unit_replace(str(GB * NPRI))  #流通市值
    print u'流通市值为：' + LTSZ
    LTGB = unit_replace(str(GB))
    print u'流通股本为：' + LTGB
    money_flow = get_today_money_flow("SELECT TOP 1 ZL_BUY_VAL,ZL_SELL_VAL,ZL_NET,YZ_BUY_VAL,YZ_SELL_VAL,YZ_NET FROM  QW_STK_CAP_HIS  WITH (NOLOCK)  "
                                  "where STOCKCODE =" + repr(stock_code[2:]) + " ORDER BY SEQ DESC ")
    ZL_BUY = unit_replace(float(money_flow[0]))
    print u'主力流入：' + ZL_BUY   #主力
    ZL_SELL = unit_replace(float(money_flow[1]))
    print u'主力流出：' + ZL_SELL
    ZL_NET = unit_replace(float(money_flow[2]))
    print u'主力净量：' + ZL_NET
    YZ_BUY = unit_replace(float(money_flow[3]))
    print u'游资流入：' + YZ_BUY
    YZ_SELL = unit_replace(float(money_flow[4]))
    print u'游资流出：' + YZ_SELL
    YZ_NET = unit_replace(float(money_flow[5]))
    print u'游资净量：' + YZ_NET
    order_moneyfolw = get_today_money_flow("  SELECT TOP 1 HUG_BUY_VAL AS '特大单流入', HUG_SELL_VAL AS '特大单流出',"
                                        "BIG_BUY_VAL AS '大单流入',BIG_SELL_VAL  AS'大单流出',MID_BUY_VAL  AS '中单流入',"
                                        "MID_SELL_VAL AS '中单流出', SML_BUY_VAL AS '小单流入'	,SML_SELL_VAL  AS'小单流出'"
                                        "FROM QW_STK_TRD_STAT  WITH (NOLOCK)  where STOCKCODE =" + repr(stock_code[2:]) + " ORDER BY SEQ DESC ")
    HUG_BUY_VAL = unit_replace(order_moneyfolw[0])
    print u'特大单流入：' + HUG_BUY_VAL
    HUG_SELL_VAL = unit_replace(order_moneyfolw[1])
    print u'特大单流出：' + HUG_SELL_VAL
    HUG_NET = unit_replace(order_moneyfolw[0]-order_moneyfolw[1])
    print u'特大单净量：' + HUG_NET

    BIG_BUY_VAL = unit_replace(order_moneyfolw[2])
    print u'大单流入：' + BIG_BUY_VAL
    BIG_SELL_VAL = unit_replace(order_moneyfolw[3])
    print u'大单流出：' + BIG_SELL_VAL
    BIG_NET = unit_replace(order_moneyfolw[2]-order_moneyfolw[3])
    print u'大单净量：' + BIG_NET

    MID_BUY_VAL = unit_replace(order_moneyfolw[4])
    print u'中单流入：' + MID_BUY_VAL
    MID_SELL_VAL = unit_replace(order_moneyfolw[5])
    print u'中单流出：' + MID_SELL_VAL
    MID_NET = unit_replace(order_moneyfolw[4]-order_moneyfolw[5])
    print u'中单净量：' + MID_NET

    SML_BUY_VAL = unit_replace(order_moneyfolw[6])
    print u'小单流入：' + SML_BUY_VAL
    SML_SELL_VAL = unit_replace(order_moneyfolw[7])
    print u'小单流出：' + SML_SELL_VAL
    SML_NET = unit_replace(order_moneyfolw[6]-order_moneyfolw[7])
    print u'小单净量：' + SML_NET

    print u'今日主力动向：' + ZL_NET
    print u'近期游资动向：' + YZ_NET


if __name__ == "__main__":
    Get_stock_detail('sz002023')  #传入股票代码
os.system("pause")  # 运行shell命令，通过执行操作系统的命令来让程序暂停
