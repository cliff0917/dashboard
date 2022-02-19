import time
import dash
import pandas as pd
import dash_datetimepicker
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from datetime import datetime
from pymongo import MongoClient
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State, ALL

import globals
from components import table, graph, collapse_item

global table, graph, df
table = table.table
graph = graph.graph
df = collapse_item.df

date_picker = dbc.Row(
    [
        dash_datetimepicker.DashDatetimepicker(id="datetime-picker"),
        html.Button('Update', id='submit_date', style={'margin-left':'1rem'}, n_clicks=0),
    ],
    style={'margin-left':'5px'}
)

datetime_output = html.H6(id='datetime-output', style={'margin-top': '20px', 'margin-left': '7px',})
dataNum = html.H3(f'{len(df)} hits', style={'textAlign': 'center'}, id='dateNum')

date = dbc.Col(
    [
        date_picker,
        datetime_output,
        dataNum,
    ],
    id='date',
)

# 修正8小時時差並轉成string
def localTime(time):
    dateFormat = '%Y-%m-%dT%H:%M:%S.%f'
    local = (pd.to_datetime(time) + pd.Timedelta(hours=8)).strftime(dateFormat)
    local = local[:-3] + '+0800'
    return local


@callback(
    [
        Output('graph', 'figure'),
        Output('datetime-output', 'children'),
        Output('dateNum', 'children'),
        Output('table', 'data'),
    ],
    [
        Input('submit_date', 'n_clicks'),
        Input('datetime-picker', 'startDate'),
        Input('datetime-picker', 'endDate'),
    ]
)
def update(n_clicks, startDate, endDate):
   
    if n_clicks == globals.update_next_clicks:
        globals.update_next_clicks += 1
        if startDate > endDate:
            return [{}, '起始時間必須大於結束時間', '', pd.DataFrame().to_dict('record')]

        startDate = localTime(startDate)
        endDate = localTime(endDate)
        posts = globals.posts

        dateFormat = "%Y-%m-%dT%H:%M:%S.%f%z"
        first_time = datetime.strptime(startDate, dateFormat)
        last_time = datetime.strptime(endDate, dateFormat)

        intervals = list(pd.date_range(startDate, endDate, freq="30min"))

        for i in range(len(intervals)):
            intervals[i] = str(intervals[i])
            date, time = intervals[i].split(' ')
            day_time, _ = time.split('+')
            intervals[i] =  date + 'T' + day_time[:-3] + '+0800'
        intervals.append(endDate)

        cnt = []
        for i in range(1, len(intervals[:-1])):
            result = posts.count_documents({'$and':[{'timestamp':{"$gte":intervals[i-1]}},{'timestamp':{"$lt":intervals[i]}}]})
            cnt.append(result)

        # 特殊處理無法被完美切割的最後一個 interval
        result = posts.count_documents({'$and':[{'timestamp':{"$gt":intervals[-2]}},{'timestamp':{"$lte":intervals[-1]}}]})
        cnt.append(result)

        dataNum = sum(cnt)
        if dataNum == 0:
            return [{}, f'從 {startDate} 到 {endDate}', '0 hits', pd.DataFrame().to_dict('record')]

        data = posts.find({'$and':[{'timestamp':{"$gte":startDate}},{'timestamp':{"$lte":endDate}}]}, {'_id':0})
        df = pd.json_normalize(data).to_dict('records')
        fig = px.bar(x=intervals[:-1], y=cnt, labels={'x': 'Time', 'y':'Count'})
        return [fig, f'從 {startDate} 到 {endDate}', f'{sum(cnt)} hits', df]

    return [dash.no_update, dash.no_update, dash.no_update, dash.no_update]
