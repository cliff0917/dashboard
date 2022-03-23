import feffery_antd_components as fac
import dash_bootstrap_components as dbc
from dash import html
from datetime import datetime, timedelta

from components import alert

# 新的 timepicker 統一 time format
def current_time():
    dateFormat = "%Y-%m-%d %H:%M:%S"
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    yesterday = yesterday.strftime("%Y-%m-%d %H:%M:%S")
    return yesterday, now

def discover_date_picker():
    # 取得現在時間
    yesterday, now = current_time()

    # discover 的 date_picker
    date_picker = dbc.Row(
        [
            fac.AntdDateRangePicker(locale='en-us', showTime=True, defaultValue=[yesterday, now], id='datetime-picker'),
            html.Button('Update', id='submit_date', style={'margin-left':'1rem'}, n_clicks=0),
        ],
        style={'margin-left':'5px'}
    )

    datetime_output = html.H6(id='datetime-output', style={'margin-top': '20px', 'margin-left': '7px'})

    date = dbc.Col(
        [
            date_picker,
            datetime_output,
        ],
    )
    return date

def se_date_picker():
    # 取得現在時間
    yesterday, now = current_time()

    # security events 的 date_picker (security events 簡稱 se)
    se_date_picker = dbc.Row(
        [
            fac.AntdDateRangePicker(locale='en-us', showTime=True, defaultValue=[yesterday, now], id='se-datetime-picker'),
            html.Button('Update', id='se-submit_date', style={'margin-left':'1rem'}, n_clicks=0),
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
    return se_date