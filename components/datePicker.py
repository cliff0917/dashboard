import dash_datetimepicker
import dash_bootstrap_components as dbc
from dash import html

# discover 的 date_picker
date_picker = dbc.Row(
    [
        dash_datetimepicker.DashDatetimepicker(id="datetime-picker"),
        html.Button('Update', id='submit_date', style={'margin-left':'1rem'}, n_clicks=0),
    ],
    style={'margin-left':'5px'}
)

datetime_output = html.H6(id='datetime-output', style={'margin-top': '20px', 'margin-left': '7px'})
hitNum = html.H1(
    [
        '載入資料中',
        dbc.Spinner(size="lg", spinner_style={'margin-left': '15px', 'width': '40px', 'height': '40px'}),
    ],
    style={'textAlign': 'center'}, id='dataNum'
)

date = dbc.Col(
    [
        date_picker,
        datetime_output,
    ],
)

# security events 的 date_picker (security events 簡稱 se)
se_date_picker = dbc.Row(
    [
        dash_datetimepicker.DashDatetimepicker(id="se-datetime-picker"),
        html.Button('Update', id='se-submit_date', style={'margin-left':'1rem', 'font-size': '15px', 'height': 37}, n_clicks=0),
    ],
    style={'margin-left':'5px'}
)

se_datetime_output = html.H6('', id='se-datetime-output', style={'margin-top': '20px', 'margin-left': '7px'})

se_date = dbc.Col(
    [
        se_date_picker,
        se_datetime_output,
    ],
)