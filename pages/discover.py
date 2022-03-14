import dash
import itertools
import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State

import globals
from process_time import process_time
from components import fields, datePicker, discover_display, collapse_item

# components
date = datePicker.date
hitNum = datePicker.hitNum
fields_bar = html.Div(fields.fields_bar)

DISPLAY_STYLE = {
    "transition": "margin-left .5s",
    "margin-top": 35,
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
    'fontSize': 10,
    'zIndex':1,
    'border':'1px black solid',
    'width': '1555px',
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
                        dcc.Loading(
                            html.Div(
                                [
                                    hitNum,
                                    dbc.Col(id='graph-and-table'),
                                ],
                            ),
                            # fullscreen=True,
                        ),
                    ],
                    style=DISPLAY_STYLE,
                ),
            ],
        ),
    ],
)

fields_btn = [Input(f'{i}', 'is_open') for i in range(len(collapse_item.add_collapse_combines))]

# 按下 Update 按鈕的觸發事件
@callback(
    [
        Output('datetime-output', 'children'),
        Output('dataNum', 'children'),
        Output("graph-and-table", "children"),
    ],
    [
        Input('submit_date', 'n_clicks'),
        fields_btn,
    ],
    [
        State('datetime-picker', 'startDate'),
        State('datetime-picker', 'endDate'),
    ]
)
def update(n_clicks, fields_btn, startDate, endDate):
    # 修正 datetime 時差, 並得到 interval
    startDate, endDate, freqs = process_time.get_freq(startDate, endDate)

    if n_clicks == globals.update_next_clicks:
        globals.update_next_clicks += 1

        if startDate >= endDate:
            return ['起始時間必須小於結束時間', '', []]

        # update display
        return discover_display.update(startDate, endDate, freqs)

    elif globals.initalization == 1:
        # initialize display
        globals.initalization = 0
        return discover_display.update(startDate, endDate, freqs)

    else:
        # 利用 fields_btn 來動態 update display
        return discover_display.update(startDate, endDate, freqs)

    return [dash.no_update for i in range(3)]