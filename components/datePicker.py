import time
import pandas as pd
import dash_datetimepicker
import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State, ALL

date_picker = dbc.Row(
    [
        dash_datetimepicker.DashDatetimepicker(id="datetime-picker"),
        html.Button('Update', id='submit_date', style={'margin-left':'1rem'}),
    ],
    style={'margin-left':'5px'}
)

datetime_output = html.H6(id='datetime-output', style={'margin-top': '20px'})

@callback(
    Output('datetime-output', 'children'),
    [
        Input('datetime-picker', 'startDate'),
        Input('datetime-picker', 'endDate'),
    ]
)
def datetime_range(startDate, endDate):
    # 修正8小時時差並轉成string
    dateFormat = '%Y-%m-%dT%H:%M:%S.%f'
    #print(startDate)
    if startDate == None or endDate == None:
        return '請重新選擇日期'
    startDate = (pd.to_datetime(startDate) + pd.Timedelta(hours=8)).strftime(dateFormat)
    startDate = startDate[:-3] + '+0800'
    endDate = (pd.to_datetime(endDate) + pd.Timedelta(hours=8)).strftime(dateFormat)
    endDate = endDate[:-3] + '+0800'
    return f'從 {startDate} 到 {endDate}'