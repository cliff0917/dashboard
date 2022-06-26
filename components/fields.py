from dash import html
import dash_bootstrap_components as dbc

from components import collapse_item

FIELD_STYLE = {
    "transition": "margin-left .5s",
    "margin-top": 35,
    "margin-left": "15px",
    "margin-right": "15px",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    'fontSize': 10,
    'width':335,
    "maxHeight": "738px",
    'zIndex':1,
    'border':'1px black solid',
    "overflow": "scroll",
}

def serve_fields():
    add_collapse_combines, del_collapse_combines = collapse_item.serve_btns()

    fields_bar =  html.Div(
        dbc.Col(
            [
                dbc.Row(
                    [
                        dbc.Col(style={"width": 50}),
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
            style=FIELD_STYLE,
        )
    )
    return fields_bar