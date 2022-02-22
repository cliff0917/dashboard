import pytz
import pandas as pd
import plotly.express as px
from pymongo import MongoClient
from datetime import datetime, timedelta

import security_event_graph
from database import connect

# 將 interval 轉成 timestamp 格式
def timestamp_format(intervals, endDate):
    for i in range(len(intervals)):
        intervals[i] = str(intervals[i])
        date, time = intervals[i].split(' ')
        day_time, _ = time.split('+')
        intervals[i] =  date + 'T' + day_time[:-3] + '+0800'

    # 將 endDate 轉成 timestamp 格式, 因為 startDate, endDate 的時間差可能無法被 freq 整除, 故要特殊處理
    # datetime.now 和 dash_datetimepicker 的時間格式不同, try 是特殊處理 datetime.now 的, 因為它中間是用空白隔開
    # 而 datetimepicker 本身就是 timestamp 格式 
    try:
        date, day_time  = endDate.split(' ')
        endDate = date + 'T' + day_time
    except:
        pass

    intervals.append(endDate)
    return intervals

def update_bar(startDate, endDate, freqs, selected_fields):
    # connect to database
    posts = connect.connect_to_db()

    # 根據 interval 切割 startDate ~ endDate
    intervals = list(pd.date_range(startDate, endDate, freq=freqs))

    # 將 selected_fields 做標記, 等等會送入 database 做查詢
    # query 負責 drop database 中任何 selected_fields 值為 null 的 row , display_cols 決定 data table 顯示哪些 column 
    query = {}
    display_cols = {'_id':0}
    for key in selected_fields:
        query[key] = {"$exists": True}
        display_cols[key] = 1

    # 轉成 timestamp 格式
    intervals = timestamp_format(intervals, endDate)

    # 計算 interval 中的 data 個數
    cnt = []
    for i in range(1, len(intervals[:-1])):
        result = posts.count_documents({'$and':[{'timestamp':{"$gte":intervals[i-1]}}, 
                                                {'timestamp':{"$lt":intervals[i]}}, 
                                                query]})
        cnt.append(result)

    # 特殊處理無法被完美切割的最後一個 interval
    result = posts.count_documents({'$and':[{'timestamp':{"$gt":intervals[-2]}}, 
                                            {'timestamp':{"$lte":intervals[-1]}}, 
                                            query]})
    cnt.append(result)

    # 找到 startDate ~ endDate 之間的所有 data, 並轉成 data table 的形式
    data = posts.find({'$and':[{'timestamp':{"$gte":startDate}}, {'timestamp':{"$lte":endDate}}, query]}, display_cols)
    df = pd.json_normalize(data)

    interval_title = security_event_graph.interval_title
    data = {'time':intervals[:-1]}
    data['Count'] = cnt
    df2 = pd.DataFrame(data)
    
    fig = px.bar(df2, x='time', y='Count', hover_data={"time":False},
                labels={'time': f'<b>timestamp per {interval_title[freqs]}</b>', 'Count':'<b>Count</b>'})
    fig.update_layout(hovermode="x unified")

    return fig, df
    # return intervals, cnt, df, len(df)

# convert datetime to string
def transfer(date):
    dateFormat = "%Y-%m-%d %H:%M:%S.%f%z"
    date = datetime.strftime(date, dateFormat)
    date = date.split('+')
    date = date[0][:-3] + '+0800'
    return date

# 得到 從昨天~現在的時間
def get_time():
    Taipei = pytz.timezone('Asia/Taipei')
    now = datetime.now(Taipei)
    yesterday = now - timedelta(days=1)

    now = transfer(now)
    yesterday = transfer(yesterday)
    return yesterday, now

# convert string to datetime format
def string_to_time(time):
    dateFormat = "%Y-%m-%dT%H:%M:%S.%f%z"
    time = datetime.strptime(time, dateFormat)
    return time

def get_freq(startDate, endDate):
    startDate = string_to_time(startDate)
    endDate = string_to_time(endDate)

    days = (endDate-startDate).days
    seconds = (endDate-startDate).seconds
    if days == 0:
        if seconds >= 1*60*60 and seconds < 3*60*60:    # 1 <= x < 3 (hours)
            freqs = '1min'
        elif seconds >= 3*60*60 and seconds < 8*60*60:  # 3 <= x < 8 (hours)
            freqs = '5min'
        elif seconds >= 8*60*60 and seconds < 17*60*60:  # 8 <= x < 17 (hours)
            freqs = '10min'
        elif seconds >= 17*60*60:   # x >= 17 (hours)
            freqs = '30min'
    elif days < 2:  #  17 <= x < 48 (hours)
        freqs = '30min'
    elif days >=2 and days < 5:
        freqs = '1H' 
    elif days >= 5 and days < 12:
        freqs = '3H'
    elif days >= 12 and days < 50:
        freqs = '12H'
    elif days >= 50 and days < 365:
        freqs = '1D'
    elif days >= 365 and days < 3*365:  # 1 <= x < 3 (years)
        freqs = '7D'
    else:  # x > 3 (years)
        freqs = '30D'
    print(freqs)
    return freqs