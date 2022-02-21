from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Jumbotron(
    [
        html.H1("404: Not found", className="text-danger"),
        html.Hr(),
        html.P(f"此網頁不存在..."),
    ]
)