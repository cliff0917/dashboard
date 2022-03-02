import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State, ALL

from components import navbar, fields, menubar, showData, datePicker

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

def serve_layout():
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
            dcc.ConfirmDialog(
                id='confirm',
                message='請先選擇fields(不選的話預設為全部的fields), 再選日期',
                displayed=True,
            ),
        ],
    )
    return layout

layout = serve_layout()