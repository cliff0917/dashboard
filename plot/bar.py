import pandas as pd
import plotly.express as px

from plot import donut
from database import get_db
from process_time import process_time

def update(startDate, endDate, freqs, selected_fields):
    # connect to database
    posts = get_db.connect_db()

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
    intervals = process_time.timestamp_format(intervals, endDate)

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

    interval_title = process_time.interval_title
    data = {'time':intervals[:-1]}
    data['Count'] = cnt
    df2 = pd.DataFrame(data)

    fig = px.bar(df2, x='time', y='Count', hover_data={"time":False},
                labels={'time': f'<b>timestamp per {interval_title[freqs]}</b>', 'Count':'<b>Count</b>'})
    fig.update_layout(hovermode="x unified")

    return fig, df

def se_update(startDate, endDate, freqs, col_name, title, top_num):
    # connect to database
    posts = get_db.connect_db()

    # 根據 interval 切割 startDate ~ endDate
    intervals = list(pd.date_range(startDate, endDate, freq=freqs))

    # 轉成 timestamp 格式
    intervals = process_time.timestamp_format(intervals, endDate)

    set_values = posts.distinct(col_name)

    cnt = [[] for i in range(len(set_values))]
    for i in range(len(set_values)):
        for j in range(1, len(intervals[:-1])):
            result = posts.count_documents({'$and':[{col_name: set_values[i]},
                                                    {'timestamp':{"$gte":intervals[j-1]}},
                                                    {'timestamp':{"$lt":intervals[j]}}]})
            cnt[i].append(result)

        # 特殊處理無法被完美切割的最後一個 interval
        result = posts.count_documents({'$and':[{col_name: set_values[i]},
                                                {'timestamp':{"$gt":intervals[-2]}},
                                                {'timestamp':{"$lte":intervals[-1]}}]})
        cnt[i].append(result)

    interval_title = process_time.interval_title
    data = {'time':intervals[:-1]}

    # 去除資料個數為零的
    non_zero_cnt = []
    non_zero_col = []
    for i in range(len(set_values)):
        if sum(cnt[i]) != 0:
            non_zero_cnt.append(cnt[i])
            non_zero_col.append(set_values[i])

    # 排序並取前 top_num 個
    non_zero_cnt, non_zero_col = donut.get_top_n(non_zero_cnt, non_zero_col, top_num)

    for i in range(len(non_zero_col)):
        data[non_zero_col[i]] = cnt[i]

    df = pd.DataFrame(data)

    fig = px.bar(df, x='time', y=non_zero_col, hover_data={"time":False}, title=f"<b>{title}</b>",
                labels={'time': f'<b>timestamp per {interval_title[freqs]}</b>', 'value':'<b>Count</b>', 'variable': ''})
    fig.update_layout(hovermode="x unified")
    fig.update_traces(hovertemplate="%{y}") # hover format = col_name : cnt

    # 將 legend 顯示在圖的右上方
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    return fig