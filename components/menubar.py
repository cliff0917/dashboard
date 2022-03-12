from dash import html
import dash_bootstrap_components as dbc

pages = ['/Home', '/Discover', '/Security-Events']
LINK_STYLE = {'color': 'blue', 'text-decoration': 'none', 'margin-right':'2rem', 'fontSize':30}

menu_bar = html.Div(
    [
        dbc.Row(
            [
                html.A('Home', href='/Home', style=LINK_STYLE),
                html.A('Discover', href='/Discover', style=LINK_STYLE),
                html.A('Security-Events', href='/Security-Events', style=LINK_STYLE),
            ],
            style={"margin-left": "6px"},
        ),
    ],
    id="menu_bar",
    style={"background-color":"#f8f9fa", 'border':'1px black solid', 'position':'fixed',  'width':'100%', 'zIndex':3},
)