import pytz
import pandas as pd
import plotly.express as px
from pymongo import MongoClient
from datetime import datetime, timedelta

from components import collapse_item

interval_title = {'30min': '30 minutes', '1H': 'hour', '3H': '3 hours', '1D': '1 day'}

# 將 interval 轉成 timestamp 格式
def timestamp_format(intervals, endDate):
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
    return intervals

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

    # 轉成 timestamp 格式
    intervals = timestamp_format(intervals, endDate)

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
    yesterday, now = get_time()

    freq = '30min'
    intervals, cnt, df, dataNum = interval_cnt(yesterday, now, freq)

    if dataNum == 0:
        return {}, f'從 {yesterday} 到 {now}', '0 hits', df

    fig = px.bar(x=intervals[:-1], y=cnt, labels={'x': 'timestamp per 30 mins', 'y':'Count'})
    return fig, f'從 {yesterday} 到 {now}', f'{dataNum} hits', df

# 得到 從昨天~現在的時間
def get_time():
    Taipei = pytz.timezone('Asia/Taipei')
    now = datetime.now(Taipei)
    yesterday = now - timedelta(days=1)

    now = transfer(now)
    yesterday = transfer(yesterday)
    return yesterday, now

def security_event_graph(startDate, endDate, col_name, freqs):
    drop_null = {col_name:{"$exists": True}}
    display_cols = {'_id':0, col_name:1}

    # connect to database
    client = MongoClient()
    db = client['pythondb']
    posts = db.posts

    # get the set of col_values
    result = posts.find(drop_null, display_cols)
    result = pd.json_normalize(result)
    result = result.squeeze()
    values = result.unique()
    try:
        values = [int(value) for value in values]
    except:
        pass

    intervals = list(pd.date_range(startDate, endDate, freq=freqs))
    intervals = timestamp_format(intervals, endDate) # 轉成 timestamp 格式

    cnt = [[] for i in range(len(values))]
    dic = {values[i]:i for i in range(len(values))}
    
    for i in range(1, len(intervals[:-1])):
        for value in values:
            result = posts.count_documents({'$and':[{'timestamp':{"$gte":intervals[i-1]}},{'timestamp':{"$lt":intervals[i]}}, {col_name:value}]})
            cnt[dic[value]].append(result)
    for value in values:
        result = posts.count_documents({'$and':[{'timestamp':{"$gt":intervals[-2]}},{'timestamp':{"$lte":intervals[-1]}}, {col_name:value}]})
        cnt[dic[value]].append(result)

    data = {'time':intervals[:-1]}
    for i in range(len(values)):
        data[values[i]] = cnt[i]
    df = pd.DataFrame(data)

    fig = px.area(df, x="time", y=values, title="<b>Alert level evolution</b>", 
              labels={"time":f"timestamp per {interval_title[freqs]}", "value": "Count", "variable": col_name},
              hover_data={"time":False}
            )
    fig.update_layout(hovermode="x unified")
    return fig

def get_area(col_name):
    yesterday, now = get_time()
    fig = security_event_graph(yesterday, now, col_name, '30min')
    return fig

# convert string to datetime format
def string_to_time(time):
    dateFormat = "%Y-%m-%dT%H:%M:%S.%f%z"
    time = datetime.strptime(time, dateFormat)
    return time

def get_freq(startDate, endDate):
    startDate = string_to_time(startDate)
    endDate = string_to_time(endDate)

    days = (endDate-startDate).days
    if days < 2:
        freqs = '30min'
    elif days >=2 and days < 5:
        freqs = '1H' 
    elif days >= 5 and days <=7:
        freqs = '3H'
    else:
        freqs = '1D'
    print(freqs)
    return freqs