import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from pymongo import MongoClient

from database import connect
from statics import timestamp_format

global interval_title
interval_title = {'30min': '30 minutes', '1H': 'hour', '3H': '3 hours', '1D': 'day'}

def update_area(startDate, endDate, col_name, freqs):
    global interval_title
    drop_null = {col_name:{"$exists": True}}
    display_cols = {'_id':0, col_name:1}

    # connect to database
    posts = connect.connect_to_db()

    # get the set of col_values
    values = posts.distinct('rule.level')

    intervals = list(pd.date_range(startDate, endDate, freq=freqs))
    intervals = timestamp_format(intervals, endDate) # 轉成 timestamp 格式

    cnt = [[] for i in range(len(values))]
    dic = {values[i]:i for i in range(len(values))}
    
    for i in range(1, len(intervals[:-1])):
        for value in values:
            result = posts.count_documents({'$and':[{'timestamp':{"$gte":intervals[i-1]}}, 
                                                    {'timestamp':{"$lt":intervals[i]}}, 
                                                    {col_name:value}]})
            cnt[dic[value]].append(result)
    for value in values:
        result = posts.count_documents({'$and':[{'timestamp':{"$gt":intervals[-2]}}, 
                                                {'timestamp':{"$lte":intervals[-1]}}, 
                                                {col_name:value}]})
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

def calculate_cnt(startDate, endDate, col_name):
    # connect to database
    posts = connect.connect_to_db()

    # get the set of col_values
    set_values = posts.distinct(col_name)

    cnt = []
    for value in set_values:
        result = posts.count_documents({'$and':[{col_name:{"$in": [value]}}, 
                                                {'timestamp':{"$gte":startDate}}, 
                                                {'timestamp':{"$lte":endDate}}]})
        cnt.append(result)
    return cnt, set_values

def update_pie(startDate, endDate, col_name):
    cnt, set_values = calculate_cnt(startDate, endDate, col_name)
    fig = go.Figure(go.Pie(
        name = col_name,
        values = cnt,
        labels = set_values,
        text = set_values,
        hovertemplate = "%{label} <br>出現次數:%{value} <br>佔比: %{percent}",
    ))
    fig.update_layout(title_text="<b>Alert</b>")
    return fig

def update_donut(startDate, endDate, col_name):
    cnt, set_values = calculate_cnt(startDate, endDate, col_name)
    fig = go.Figure(go.Pie(
        name = col_name,
        values = cnt,
        labels = set_values,
        text = set_values,
        hovertemplate = "%{label} <br>出現次數:%{value} <br>佔比: %{percent}",
        hole=0.8,
    ))
    fig.update_layout(title_text="<b>Top 5 agents</b>")
    return fig