import dash
import pandas as pd
import dash_datetimepicker
import dash_bootstrap_components as dbc
from dash import html, callback
from dash.dependencies import Input, Output

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

# security events 簡稱 se
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