import dash
import pandas as pd
import dash_datetimepicker
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, callback
from dash.dependencies import Input, Output, State, ALL

import globals, statics
from statics import interval_cnt, get_freq
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
se_datetime_output = html.H6(id='se-datetime-output', style={'margin-left': '7px'})

date = dbc.Col(
    [
        date_picker,
        datetime_output,
        dataNum,
    ],
    id='date',
)

se_date_picker = dbc.Row(
    [
        dash_datetimepicker.DashDatetimepicker(id="datetime-picker2"),
        html.Button('Update', id='submit_date2', style={'margin-left':'1rem', 'font-size': '15px', 'height': 37}, n_clicks=0),
    ],
    style={'margin-left':'5px'}
)
se_date = dbc.Col(
    [
        se_date_picker,
        se_datetime_output,
    ],
    id='date2',
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
        Output("table", "tooltip_data"),
        Output("table", "tooltip_header"),
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
        if startDate >= endDate:
            return [{}, '起始時間必須小於結束時間', '', pd.DataFrame().to_dict('record'), [], [], {}]

        # 修正 datetime 時差, 並 convert datetime to string
        startDate = localTime(startDate)
        endDate = localTime(endDate)

        # 計算每個 interval 中的 data 個數
        freqs = get_freq(startDate, endDate)
        intervals, cnt, df, dataNum = interval_cnt(startDate, endDate, freqs)
        columns = [{'name': column, 'id': column} for column in df.columns]

        tooltip_data=[
            {
                column: {'value': f'{column}\n\n{value}', 'type': 'markdown'}
                for column, value in row.items()
            } for row in df.to_dict('records')
        ]
        tooltip_header = {i: i for i in df.columns}

        if dataNum == 0:
            return [{}, f'從 {startDate} 到 {endDate}', '0 hits', df.to_dict('record'), columns, tooltip_data, tooltip_header]

        interval_title = statics.interval_title
        data = {'time':intervals[:-1]}
        data['Count'] = cnt
        df2 = pd.DataFrame(data)
        
        fig = px.bar(df2, x='time', y='Count', hover_data={"time":False},
                    labels={'time': f'<b>timestamp per {interval_title[freqs]}</b>', 'Count':'<b>Count</b>'})
        fig.update_layout(hovermode="x unified")
        return [fig, f'從 {startDate} 到 {endDate}', f'{dataNum} hits', df.to_dict('record'), columns, tooltip_data, tooltip_header]

    return [dash.no_update, f'從 {startDate} 到 {endDate}', dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update]