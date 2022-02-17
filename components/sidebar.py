from dash import html
import dash_bootstrap_components as dbc

SIDEBAR_STYLE={
    "position": "fixed",
    "top": 127.5,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 2,
    #"overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "orange",
    #"background-color": "#f8f9fa",
    'border':'1px black solid',
}

SIDEBAR_HIDDEN = {
    "position": "fixed",
    "top": 127.5,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 2,
    #"overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "orange",
    #"background-color": "#f8f9fa",
    'border':'1px black solid',
}

sidebar = html.Div(
    dbc.Col(
        [
            html.H2("Sidebar", className="display-4"),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/Home", id="page-1-link"),
                    dbc.NavLink("Discover", href="/Discover", id="page-2-link"),
                    dbc.NavLink("Security-Events", href="/Security-Events", id="page-3-link"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
    ),
    id="sidebar",
    style=SIDEBAR_STYLE,
)