import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output

import globals
from plot import area, donut, bar
from database import get_db
from process_time import process_time
from components import datePicker, graph

date = datePicker.se_date
area_chart = graph.area_chart
donut_chart1 = graph.donut_chart1
donut_chart2 = graph.donut_chart2
se_bar_chart = graph.se_bar_chart

DISPLAY_STYLE = {
    "transition": "margin-left .5s",
    "margin-top": 47,
    "margin-left": 5,
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
    'fontSize': 10,
    'zIndex':1,
    'border':'1px black solid',
    'zIndex':2,
}

COL_STYLE = {
    'fontSize':20, 
    'margin-left':155,
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
                        html.H4('--', style={'fontSize':30, 'color':'blue', 'align':'center'}, id='total'),#'margin-left':'10.5rem'
                    ],
                    style={'width':3},
                ),
                dbc.Col(
                    [
                         html.H4('Level 12 or above alerts'),
                         html.H4('--', style={'fontSize':30, 'color':'red', 'align':'center'}, id='level12'),#'margin-left':'16rem',
                    ],
                    style={'width':3},
                ),
                dbc.Col(
                    [
                        html.H4('Authentication failure'),
                        html.H4('--', style={'fontSize':30, 'color':'red', 'align':'center'}, id='fail'),#'margin-left':'16rem',
                    ],
                    style={'width':3},
                ),
                dbc.Col(
                    [
                        html.H4('Authentication success'),
                        html.H4('--', style={'fontSize':30, 'color':'green', 'align':'center'}, id='success'),#'margin-left':'17rem', 
                    ],
                    style={'width':3},
                ),
            ],
            style={'margin-top':10, 'margin-left':'10rem'},
        ),
        # dbc.Row(
        #     [
        #         html.H4('--', style={'fontSize':30,'margin-left':'11.5rem', 'color':'blue', 'align':'center'}, id='total'),
        #         html.H4('--', style={'fontSize':30,'margin-left':'34rem', 'color':'red', 'align':'center'}, id='level12'),
        #         html.H4('--', style={'fontSize':30,'margin-left':'28rem', 'color':'red', 'align':'center'}, id='fail'),
        #         html.H4('--', style={'fontSize':30,'margin-left':'30rem', 'color':'green', 'align':'center'}, id='success'),
        #     ],
        # ),
        dbc.Row(
            [
                area_chart,
                donut_chart1,
            ], 
        ),
        dbc.Row(
            [
                donut_chart2,
                se_bar_chart,
            ], 
        ),
    ],
)

# 按下 Update 按鈕的觸發事件
@callback(
    [
        Output('area_chart', 'figure'),
        Output('se-datetime-output', 'children'),
        Output('donut_chart1', 'figure'),
        Output('donut_chart2', 'figure'),
        Output('se_bar_chart', 'figure'),
        Output('total', 'children'),
        Output('level12', 'children'),
        Output('fail', 'children'),
        Output('success', 'children'),
    ],
    [
        Input('submit_date2', 'n_clicks'),
        Input('datetime-picker2', 'startDate'),
        Input('datetime-picker2', 'endDate'),
    ]
)
def update(n_clicks, startDate, endDate):
    if n_clicks == globals.update2_next_clicks:
        globals.update2_next_clicks += 1

        if startDate >= endDate:
            return [{}, '起始時間必須小於結束時間', {}, {}, {}, dash.no_update, dash.no_update, dash.no_update, dash.no_update]

        # 得到 interval
        freqs = process_time.get_freq(startDate, endDate)

        # 修正 datetime 時差, 並 convert datetime to string
        startDate = process_time.localTime(startDate)
        endDate = process_time.localTime(endDate)

        # get chart
        area_fig = area.update(startDate, endDate, 'rule.level', freqs)
        donut_fig1 = donut.update(startDate, endDate, 'rule.mitre.technique', 'Top MITRE ATT&CKS')
        donut_fig1.update_layout(legend=dict(x=1.2)) # legend 會擋到 label, 故往右移
        donut_fig2 = donut.update(startDate, endDate, 'agent.name', 'Top 5 agents')
        bar_fig, _ = bar.update(startDate, endDate, freqs, ['agent.name'])
        
        # get num
        posts = get_db.connect_db()
        total = posts.count_documents({'$and':[{'timestamp':{"$gte":startDate}},
                                               {'timestamp':{"$lte":endDate}}]})

        level12 = posts.count_documents({'$and':[{'timestamp': {"$gte":startDate}},
                                                 {'timestamp': {"$lte":endDate}},
                                                 {'rule.level':{"$gte":12}}]})

        fail = posts.count_documents({'$and':[{'timestamp':{"$gte":startDate}},
                                              {'timestamp':{"$lte":endDate}},
                                              {'rule.groups':'authentication_failed'}]})

        success = posts.count_documents({'$and':[{'timestamp':{"$gte":startDate}},
                                                 {'timestamp':{"$lte":endDate}},
                                                 {'rule.groups':'authentication_success'}]})

        return [area_fig, f'從 {startDate} 到 {endDate}', donut_fig1, donut_fig2, bar_fig, total, level12, fail, success]

    # 已經有按過 update, 但不等於 next_click, 代表 user 正在選日期 => page info 皆不變
    elif n_clicks:
        return [dash.no_update for i in range(9)]

    return [{}, '請選取時間', {}, {}, {}, dash.no_update, dash.no_update, dash.no_update, dash.no_update]