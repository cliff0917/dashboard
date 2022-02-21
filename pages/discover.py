import dash
from dash import dcc, html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL

from components import collapse_item, navbar, sidebar, fields, menubar, table, graph, showData, datePicker

url = dcc.Location(id="url")
all_pages = ['/Home','/Discover','/Security-Events']

# styles
# SIDEBAR_STYLE = sidebar.SIDEBAR_STYLE
# SIDEBAR_HIDDEN = sidebar.SIDEBAR_HIDDEN
# FIELD_STYLE = fields.FIELD_STYLE
# FIELD_STYLE1 = fields.FIELD_STYLE1

# components
navbar = navbar.navbar
menu_bar = menubar.menu_bar
show_data = showData.show_data
date = datePicker.date

# field = html.Div(
#     id="page-content",
# )

# content = html.Div(
#     [
#         dbc.Row(
#             [
#                 field,
#                 show_data,
#             ],
#         )
#     ],
#     id='content',
# )

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

# 當 btn_sidebar 觸發時, sidebar 和 content 的位置會發生改變
# @callback(
#     [
#         Output("sidebar", "style"),
#         Output("page-content", "style"),
#         Output("side_click", "data"),
#     ],
#     [
#         Input("btn_Sidebar", "n_clicks"),
#     ],
#     [
#         State("side_click", "data"),
#     ]
# )
# def toggle_sidebar(n, nclick):
#     if n:
#         if nclick == "SHOW":
#             sidebar_style = SIDEBAR_HIDDEN
#             field_style = FIELD_STYLE1
#             cur_nclick = "HIDDEN"
#         else:
#             sidebar_style = SIDEBAR_STYLE
#             field_style = FIELD_STYLE
#             cur_nclick = "SHOW"
#     else:
#         sidebar_style = SIDEBAR_STYLE
#         field_style = FIELD_STYLE
#         cur_nclick = 'SHOW'

#     return sidebar_style, field_style, cur_nclick