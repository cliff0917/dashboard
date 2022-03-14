import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output

import globals
from process_time import process_time
from components import datePicker, se_display

date = datePicker.se_date

DISPLAY_STYLE = {
    "transition": "margin-left .5s",
    "margin-top": 47,
    "margin-left": 5,
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
    'fontSize': 10,
    'zIndex': 1,
    'border': '1px black solid',
    'zIndex': 2,
}

COL_STYLE = {
   'width': 3,
   'textAlign': 'center',
}

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        date,
                    ],
                    style=DISPLAY_STYLE,
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4('Total'),
                        html.H4('--', style={'fontSize':30, 'color':'blue'}, id='total'),
                    ],
                    style=COL_STYLE,
                ),
                dbc.Col(
                    [
                         html.H4('Level 12 or above alerts'),
                         html.H4('--', style={'fontSize':30, 'color':'red'}, id='level12'),
                    ],
                    style=COL_STYLE,
                ),
                dbc.Col(
                    [
                        html.H4('Authentication failure'),
                        html.H4('--', style={'fontSize':30, 'color':'red'}, id='fail'),
                    ],
                    style=COL_STYLE,
                ),
                dbc.Col(
                    [
                        html.H4('Authentication success'),
                        html.H4('--', style={'fontSize':30, 'color':'green'}, id='success'),
                    ],
                    style=COL_STYLE,
                ),
            ],
            style={'margin-top':10},
        ),
        dcc.Loading(
            [
                dbc.Row(
                    id='graph-frist-row',
                ),
                dbc.Row(
                    id='graph-second-row',
                ),
            ],
            fullscreen=True,
        ),
    ],
)

# 按下 Update 按鈕的觸發事件
@callback(
    [
        Output('se-datetime-output', 'children'),
        Output('total', 'children'),
        Output('level12', 'children'),
        Output('fail', 'children'),
        Output('success', 'children'),
        Output('graph-frist-row', 'children'),
        Output('graph-second-row', 'children'),
    ],
    [
        Input('se-submit_date', 'n_clicks'),
        Input('se-datetime-picker', 'startDate'),
        Input('se-datetime-picker', 'endDate'),
    ]
)
def update(n_clicks, startDate, endDate):
    # 修正 datetime 時差, 並得到 interval
    startDate, endDate, freqs = process_time.get_freq(startDate, endDate)

    if n_clicks == globals.update2_next_clicks:
        globals.update2_next_clicks += 1

        if startDate >= endDate:
            status = [dash.no_update for i in range(6)]
            status.insert(0, '起始時間必須小於結束時間')
            return status

        # update display
        return se_display.update(startDate, endDate, freqs)


    elif globals.initalization == 1:
        # initialize display
        globals.initalization = 0
        return se_display.update(startDate, endDate, freqs)

    return [dash.no_update for i in range(7)]