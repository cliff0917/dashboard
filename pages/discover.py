import dash
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output

import globals, security_event_graph
from statics import update_bar, get_freq
from components import navbar, fields, menubar, showData, datePicker, table, collapse_item

# components
navbar = navbar.navbar
menu_bar = menubar.menu_bar
show_data = showData.show_data
date = datePicker.date

fields_bar = html.Div(
    fields.fields_bar,
)

DISPLAY_STYLE = {
    "transition": "margin-left .5s",
    "margin-top": 35,
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
    'fontSize': 10,
    'zIndex':1,
    'border':'1px black solid',
    'width': '900px',
    'zIndex':1,
}

layout = html.Div(
    [
        dbc.Row(
            [
                fields_bar,
                dbc.Col(
                    [
                        date,
                        show_data,
                    ],
                    style=DISPLAY_STYLE,
                ), 
            ],
        ),
    ],
)

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
        startDate = datePicker.localTime(startDate)
        endDate = datePicker.localTime(endDate)

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

    return [{}, '請先選擇fields(不選的話預設為全部的fields), 再選時間', '0 hits', pd.DataFrame().to_dict('record'), [], dash.no_update, dash.no_update]