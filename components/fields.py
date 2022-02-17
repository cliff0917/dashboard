from dash import html
import dash_bootstrap_components as dbc

from components import collapse_item

# FIELD_STYLE 為 sideBar 顯示時, field 的 style
# FIELD_STYLE1 為 sideBar 隱藏時, field 的 style
# FIELD_STYLE = {
#     "transition": "margin-left .5s",
#     "margin-top": 55,
#     "margin-left": "18rem",
#     "margin-right": "1rem",
#     "padding": "2rem 1rem",
#     "background-color": "yellow",
#     'fontSize': 10,
#     #'width': 284,
#     'width': 300,
#     "maxHeight": "720px",
#     'zIndex':1,
#     'border':'1px black solid',
#     "overflow": "scroll",
# }

# FIELD_STYLE1 = {
#     "transition": "margin-left .5s",
#     "margin-top": 55,
#     "margin-left": "2rem",
#     "margin-right": "1rem",
#     "padding": "2rem 1rem",
#     "background-color": "yellow",
#     'fontSize': 10,
#     #'width':284,
#     'width': 300,
#     "maxHeight": "720px",
#     'zIndex':1,
#     'border':'1px black solid',
#     "overflow": "scroll",
# }

NEW_FIELD_STYLE = {
    "transition": "margin-left .5s",
    "margin-top": 35,
    "margin-left": "15px",
    "margin-right": "15px",
    "padding": "2rem 1rem",
    "background-color": "yellow",
    'fontSize': 10,
    'width':284,
    #'width': 300,
    "maxHeight": "738px",
    'zIndex':1,
    'border':'1px black solid',
    "overflow": "scroll",
}

OTHER_FIELD_STYLE = {
    "transition": "margin-left .5s",
    "margin-top": 35,
    #"margin-left": "15px",
    #"margin-right": "15px",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    'fontSize': 40,
    #'width':284,
    #'width': 300,
    #"maxHeight": "738px",
    'zIndex':1,
    'border':'1px black solid',
    #"overflow": "scroll",
}

add_collapse_combines = collapse_item.add_collapse_combines
del_collapse_combines = collapse_item.del_collapse_combines

fields_bar = dbc.Col(
    [
        dbc.Row(
            [
                dbc.Col(style={"width": 50}),
                dbc.Button('Enter', id='submit_fields')
                #html.Img(src=btn_field, width=50, id='btn_field')
            ],
        ),
        dbc.Container(
            [
                dbc.Row(
                    [
                        html.B('Selected fields:', style={'fontSize':20})      
                    ],
                ),
                dbc.Row(
                    [
                        del_collapse_combine for del_collapse_combine in del_collapse_combines
                    ],
                ),
                html.Hr(style={'borderColor':'black'}),
                dbc.Row(
                    [
                        html.B('Available fields:', style={'fontSize':20})
                    ],
                ),
                dbc.Row(
                    [
                        add_collapse_combine for add_collapse_combine in add_collapse_combines
                    ],
                ),
            ],
        ),
    ],
    id='fields_bar',
    style=NEW_FIELD_STYLE,
),