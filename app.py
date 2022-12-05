import warnings

warnings.filterwarnings("ignore", category=Warning)

import os
import dash
import webbrowser
from dash import dcc, html, callback
from dash.dependencies import Input, Output
from flask import send_from_directory

import globals
from components import navbar, sidebar, lottie
from pages import home, discover, security_events, non_exist

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# global first
# first = 1

CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "15.5rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "position":"relative",
    "left":'0.2rem',
    'fontSize': 30,
    'zIndex':1,
}

# components
navbar = navbar.navbar
sidebar = sidebar.sidebar
url = dcc.Location(id="url")
content = html.Div(id='content', style=CONTENT_STYLE)

def serve_layout():
    # 得到最新狀態的 db
    globals.initialize()

    layout = html.Div(
        [
            url,
            navbar,
            sidebar,
            content,
        ],
    )
    return layout

# live update, 請注意這裡是要用 serve_layout 而非 serve_layout()
app.layout = serve_layout
server = app.server
server = lottie.serve_lottie(server)

# 透過 url 來決定顯示哪個 page
@callback(
    Output('content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    # live update layout
    if pathname in ['/', '/Home']:
        return home.serve_layout()

    elif pathname == '/Discover':
        layout = discover.serve_layout()
        return layout

    elif pathname == '/Security-Events':
        layout = security_events.serve_layout()
        return layout

    return non_exist.serve_layout()  # 若非以上路徑, 則 return 404 message

if __name__ == '__main__':
    debug = 1

    if debug == 1:
        app.run_server(debug=True, dev_tools_props_check=False) # debug mode
    else:
        pid = os.fork()
        if pid != 0:
            app.run_server()
        else:
            url = "http://127.0.0.1:8050/"
            webbrowser.open(url)