import pytz
import pandas as pd
import plotly.express as px
from pymongo import MongoClient
from datetime import datetime, timedelta

from components import collapse_item

def interval_cnt(startDate, endDate, freqs):
    # connect to database
    client = MongoClient()
    db = client['pythondb']
    posts = db.posts

    # 根據 interval 切割 startDate ~ endDate
    intervals = list(pd.date_range(startDate, endDate, freq=freqs))

    # 將 selected_fields 做標記, 等等會送入 database 做查詢
    # query 負責 drop database 中任何 selected_fields 值為 null 的 row , display_cols 決定 data table 顯示哪些 column 
    query = {}
    display_cols = {'_id':0}
    selected_fields = collapse_item.selected_fields
    for key in selected_fields:
        query[key] = {"$exists": True}
        display_cols[key] = 1

    # 將 interval 轉成 timestamp 格式
    for i in range(len(intervals)):
        intervals[i] = str(intervals[i])
        date, time = intervals[i].split(' ')
        day_time, _ = time.split('+')
        intervals[i] =  date + 'T' + day_time[:-3] + '+0800'
    
    # 將 endDate 轉成 timestamp 格式, 因為 startDate, endDate 的時間差可能無法被 freq 整除, 故要特殊處理
    # datetime.now 和 dash_datetimepicker 的時間格式不同, try 是特殊處理 datetime.now 的, 因為它中間是用空白隔開, 而 datetimepicker 本身就是 timestamp 格式 
    try:
        date, day_time  = endDate.split(' ')
        endDate = date + 'T' + day_time
    except:
        pass
    intervals.append(endDate)

    # 計算 interval 中的 data 個數
    cnt = []
    for i in range(1, len(intervals[:-1])):
        result = posts.count_documents({'$and':[{'timestamp':{"$gte":intervals[i-1]}},{'timestamp':{"$lt":intervals[i]}}, query]})
        cnt.append(result)

    # 特殊處理無法被完美切割的最後一個 interval
    result = posts.count_documents({'$and':[{'timestamp':{"$gt":intervals[-2]}},{'timestamp':{"$lte":intervals[-1]}}, query]})
    cnt.append(result)

    # 找到 startDate ~ endDate 之間的所有 data, 並轉成 data table 的形式
    data = posts.find({'$and':[{'timestamp':{"$gte":startDate}},{'timestamp':{"$lte":endDate}}, query]}, display_cols)
    df = pd.json_normalize(data)

    return intervals, cnt, df, len(df)

# convert datetime to string
def transfer(date):
    dateFormat = "%Y-%m-%d %H:%M:%S.%f%z"
    date = datetime.strftime(date, dateFormat)
    date = date.split('+')
    date = date[0][:-3] + '+0800'
    return date

# 初始化最一開始的圖, 計算從昨天~現在的 data ,interval=30分
def get_one_day():
    Taipei = pytz.timezone('Asia/Taipei')
    now = datetime.now(Taipei)
    yesterday = now - timedelta(days=1)

    now = transfer(now)
    yesterday = transfer(yesterday)

    freq = '30min'
    intervals, cnt, df, dataNum = interval_cnt(yesterday, now, freq)

    if dataNum == 0:
        return {}, f'從 {yesterday} 到 {now}', '0 hits', df

    fig = px.bar(x=intervals[:-1], y=cnt, labels={'x': 'Time', 'y':'Count'})
    return fig, f'從 {yesterday} 到 {now}', f'{dataNum} hits', df