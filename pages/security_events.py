import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State, ALL

import globals
from components import datePicker, fields, graph
from statics import get_freq, update_bar
from security_event_graph import update_area, update_pie, update_donut

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

@callback(
    [
        Output('area_chart', 'figure'),
        Output('se-datetime-output', 'children'),
        Output('donut_chart1', 'figure'),
        Output('donut_chart2', 'figure'),
        Output('se_bar_chart', 'figure'),
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
            return [{}, '起始時間必須小於結束時間', {}, {}, {}]

        # 得到 interval
        freqs = get_freq(startDate, endDate)

        # 修正 datetime 時差, 並 convert datetime to string
        startDate = datePicker.localTime(startDate)
        endDate = datePicker.localTime(endDate)

        # get chart
        area_fig = update_area(startDate, endDate, 'rule.level', freqs)
        donut_fig1 = update_donut(startDate, endDate, 'rule.mitre.technique', 'Alert')
        donut_fig2 = update_donut(startDate, endDate, 'agent.name', 'Top 5 agents')
        bar_fig, _ = update_bar(startDate, endDate, freqs, ['agent.name'])

        donut_fig1.update_layout(legend=dict(x=1.2)) # legend 會擋到 label, 故往左移
        return [area_fig, f'從 {startDate} 到 {endDate}', donut_fig1, donut_fig2, bar_fig]

    # 已經有按過 update, 但不等於 next_click, 代表 user 正在選日期 => page info 皆不變
    elif n_clicks:
        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update]

    return [{}, '請選取時間', {}, {}, {}]