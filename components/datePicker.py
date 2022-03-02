import dash
import pandas as pd
import dash_datetimepicker
import dash_bootstrap_components as dbc
from dash import html, callback
from dash.dependencies import Input, Output, State, ALL

import globals, security_event_graph
from statics import update_bar, get_freq
from components import table, graph, collapse_item

table = table.table
bar_chart = graph.bar_chart

date_picker = dbc.Row(
    [
        dash_datetimepicker.DashDatetimepicker(id="datetime-picker"),
        html.Button('Update', id='submit_date', style={'margin-left':'1rem'}, n_clicks=0),
    ],
    style={'margin-left':'5px'}
)

datetime_output = html.H6(id='datetime-output', style={'margin-top': '20px', 'margin-left': '7px',})
hitNum = html.H3(style={'textAlign': 'center'}, id='dataNum')
se_datetime_output = html.H6(id='se-datetime-output', style={'margin-top': '20px', 'margin-left': '7px'})

date = dbc.Col(
    [
        date_picker,
        datetime_output,
        hitNum,
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
        Output('bar_chart', 'figure'),
        Output('datetime-output', 'children'),
        Output('dataNum', 'children'),
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
            return [{}, '起始時間必須小於結束時間', '', pd.DataFrame().to_dict('record'), [], dash.no_update, dash.no_update]

        # 修正 datetime 時差, 並 convert datetime to string
        startDate = localTime(startDate)
        endDate = localTime(endDate)

        # 計算每個 interval 中的 data 個數
        freqs = get_freq(startDate, endDate)
        bar_fig, df = update_bar(startDate, endDate, freqs, collapse_item.selected_fields)
        columns = [{'name': column, 'id': column} for column in df.columns]

        tooltip_data=[
            {
                column: {'value': f'{column}\n\n{value}', 'type': 'markdown'}
                for column, value in row.items()
            } for row in df.to_dict('records')
        ]
        tooltip_header = {i: i for i in df.columns}

        # 解決 data table 中 list 的顯示問題, 將 df 中的 list 轉成 string 用逗號隔開, 並串接在一起
        for column in list(df.columns):
            df[column] = [', '.join(map(str, l)) if isinstance (l, list) else l for l in df[column]]

        return [bar_fig, f'從 {startDate} 到 {endDate}', f'{len(df)} hits', df.to_dict('record'), columns, tooltip_data, tooltip_header]

    # 已經有按過 update, 但不等於 next_click, 代表 user 正在選日期 => page info 皆不變
    elif n_clicks:
        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update]

    return [{}, '請選取時間', '0 hits', pd.DataFrame().to_dict('record'), [], dash.no_update, dash.no_update]