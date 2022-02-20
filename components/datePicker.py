import dash
import pandas as pd
import dash_datetimepicker
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, callback
from dash.dependencies import Input, Output, State, ALL

import globals
from statics import interval_cnt
from components import table, graph

table = table.table
dataCnt = graph.dataCnt
graph = graph.graph

date_picker = dbc.Row(
    [
        dash_datetimepicker.DashDatetimepicker(id="datetime-picker"),
        html.Button('Update', id='submit_date', style={'margin-left':'1rem'}, n_clicks=0),
    ],
    style={'margin-left':'5px'}
)

datetime_output = html.H6(id='datetime-output', style={'margin-top': '20px', 'margin-left': '7px',})
dataNum = html.H3(f'{dataCnt} hits', style={'textAlign': 'center'}, id='dateNum')

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

# 按下 Update 按鈕的觸發事件
@callback(
    [
        Output('graph', 'figure'),
        Output('datetime-output', 'children'),
        Output('dateNum', 'children'),
        Output('table', 'data'),
        Output('table', 'columns'),
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
            return [{}, '起始時間必須大於結束時間', '', pd.DataFrame().to_dict('record'), []]

        # 修正 datetime 時差, 並 convert datetime to string
        startDate = localTime(startDate)
        endDate = localTime(endDate)

        # 計算每個 interval 中的 data 個數
        freqs = '30min'
        intervals, cnt, df, dataNum = interval_cnt(startDate, endDate, freqs)
        columns = [{'name': column, 'id': column} for column in df.columns]

        if dataNum == 0:
            return [{}, f'從 {startDate} 到 {endDate}', '0 hits', df.to_dict('record'), columns]

        fig = px.bar(x=intervals[:-1], y=cnt, labels={'x': 'Time', 'y':'Count'})
        return [fig, f'從 {startDate} 到 {endDate}', f'{dataNum} hits', df.to_dict('record'), columns]

    return [dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update]