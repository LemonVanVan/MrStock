#-*- coding: utf8 -*-
import datetime,MySQLdb,re,time
def get_date(day):
    holiday = []
    try:
        conn = MySQLdb.connect(host='192.168.10.230', port=3306, user='stocksir', passwd='stocksir1704!', db='stocksir')
        cursor = conn.cursor()
        holiday_sql = "SELECT `value` FROM `stock_setting` WHERE `name`= 'holiday'"   #查询法定节假日
        cursor.execute(holiday_sql)
        for i in cursor.fetchall():
            pass
    except Exception as error:
        print error

    day_list = (list(i))[0]   #查询获得的节假日转换为字符串
    holiday_list = re.findall('s:4:"name";s:10:"(.+?)";s:5:"intro";', day_list)  #正则匹配出所有节假日，存入holiday_list数组，日期为时间戳格式
    for index in holiday_list:
        holiday.append(time.strftime("%Y-%m-%d",time.localtime(int(index))))     #将时间戳转为日期xx-xx-xx格式，存入holiday数组
    # print holiday
    now_time = datetime.date.today()  #获取当天日期

    #print now_time
    # history_data = now_time - datetime.timedelta(days=0) #日期加减  .weekday()当前日期星期几
    # print history_data
    week_day = [5,6]  #值：5、6分别代表：星期六、星期天
    count = 0
    hour_time = int(time.strftime('%H', time.localtime(time.time())))
    if hour_time > 15:  #盘中时间大于下午15点，计算日期为当天前一天
        for i in range(100):
            history_data = now_time - datetime.timedelta(days=i+1)
            if history_data.weekday() not in week_day: #排除周末
                if str(history_data) not in holiday:  #排除节假日
                    #print str(history_data)
                    count = count + 1
                    if count == day:
                        break
        count_date = str(history_data).replace('-', '')   #count_date为参与累计收益计算日期

        return count_date
    else:  #计算时间小于当天15点，计算日期为当天日期的前2天
        for i in range(100):
            history_data = now_time - datetime.timedelta(days=i+2)
            if history_data.weekday() not in week_day:  #排除周末
                if str(history_data) not in holiday:    #排除节假日
                    # print str(history_data)
                    count = count + 1
                    print count
                    if count == day:
                        break

        count_date = str(history_data).replace('-','')  #count_date为参与累计收益计算日期

        return count_date
def plan_rate(date,plan_class):   #根据30日的有效日期，计算出30天的累计收益
    try:
        now_time = str(datetime.date.today()).replace('-', '')
        conn = MySQLdb.connect(host='192.168.10.230',port=3306,user='stocksir',passwd='stocksir1704!',db='stocksir')
        cursor = conn.cursor()
        plan_stock_sql = "SELECT SUM(max_rate) FROM `stock_plan_stock` WHERE plan_id IN" + \
                         "(SELECT id FROM `stock_plan` WHERE plan_class_id =" + str(plan_class) + " AND `date` >=" + date + " AND `date` <" + now_time + ")"
        cursor.execute(plan_stock_sql)
        for count_rate in cursor.fetchall():
            pass
        print "股机实际（未加权）累计收益为：" + str(count_rate[0])

    except Exception as error:
        print error

if __name__ == "__main__":
    plan_rate(get_date(30),87)  #传入股机累计收益计算天数，和股机类型：85（股机A），86（股机B），87(股机C)

