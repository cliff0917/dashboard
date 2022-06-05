import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
from dash_extensions import Lottie

from process_time import process_time
from components import datePicker, se_display, alert

options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))

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

def serve_layout(first):
    first, notification = alert.update_notification(first)

    layout = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    datePicker.se_date_picker(), # live update
                                    notification,
                                ],
                            )
                        ],
                        style=DISPLAY_STYLE,
                    ),
                ],
            ),
            dcc.Loading(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(Lottie(options=options, width="23%", height="23%", url="/total", speed=2)),
                                        dbc.CardBody(
                                            [
                                                html.H4('Total'),
                                                html.H4('--', style={'fontSize':30, 'color':'blue'}, id='total'),
                                            ],
                                        ),
                                    ],
                                ),
                                style=COL_STYLE,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(Lottie(options=options, width="15%", height="15%", url="/alert", speed=1)),
                                        dbc.CardBody(
                                            [
                                                html.H4('Level 12 or above alerts'),
                                                html.H4('--', style={'fontSize':30, 'color':'red'}, id='level12'),
                                            ],
                                        ),
                                    ],
                                ),
                                style=COL_STYLE,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(Lottie(options=options, width="17%", height="17%", url="/failure", speed=0.595)),
                                        dbc.CardBody(
                                            [
                                                html.H4('Authentication failure'),
                                                html.H4('--', style={'fontSize':30, 'color':'red'}, id='fail'),
                                            ],
                                        ),
                                    ],
                                ),
                                style=COL_STYLE,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(Lottie(options=options, width="17%", height="17%", url="/success", speed=0.8)),
                                        dbc.CardBody(
                                            [
                                                html.H4('Authentication success'),
                                                html.H4('--', style={'fontSize':30, 'color':'green'}, id='success'),
                                            ],
                                        ),
                                    ],
                                ),
                                style=COL_STYLE,
                            ),
                        ],
                        style={'margin-top':10},
                    ),
                    dbc.Row(
                        id='graph-frist-row',
                    ),
                    dbc.Row(
                        id='graph-second-row',
                    ),
                ],
            ),
        ],
    )
    return first, layout

# 初始化 display or 按下 Update 按鈕的觸發事件
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
    ],
    [
        State('se-datetime-picker', 'value')
    ]
)
def update(n_clicks, time):
    # 將 time 轉成 timestamp format, 並得到 interval
    startDate, endDate, freqs = process_time.get_time_info(time)
    return se_display.update(startDate, endDate, freqs)
