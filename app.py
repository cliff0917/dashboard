import warnings

warnings.filterwarnings("ignore", category=Warning)

import os
import dash
import webbrowser
from dash import dcc, html, callback
from dash.dependencies import Input, Output
from flask import send_from_directory

import globals
from components import navbar, menubar
from pages import home, discover, security_events, non_exist

app = dash.Dash(__name__, suppress_callback_exceptions=True)

global first
first = 1

# components
navbar = navbar.navbar
menu_bar = menubar.menu_bar
url = dcc.Location(id="url")
content = html.Div(id='content')

def serve_layout():
    # 得到最新狀態的 db
    globals.initialize()

    layout = html.Div(
        [
            url,
            navbar,
            menu_bar,
            content,
        ],
    )
    return layout

# live update, 請注意這裡是要用 serve_layout 而非 serve_layout()
app.layout = serve_layout
server = app.server

# 透過 url 來決定顯示哪個 page
@callback(
    Output('content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    global first

    # live update layout
    if pathname in ['/', '/Home']:
        return home.serve_layout()

    elif pathname == '/Discover':
        first, layout = discover.serve_layout(first)
        return layout

    elif pathname == '/Security-Events':
        first, layout = security_events.serve_layout(first)
        return layout

    return non_exist.serve_layout()  # 若非以上路徑, 則 return 404 message

@server.route("/total", methods=['GET'])
def serving_lottie_total():
    directory = os.path.join(os.getcwd(), "assets/lottie")
    return send_from_directory(directory, "total.json")

@server.route("/alert", methods=['GET'])
def serving_lottie_alert():
    directory = os.path.join(os.getcwd(), "assets/lottie")
    return send_from_directory(directory, "alert.json")

@server.route("/failure", methods=['GET'])
def serving_lottie_failure():
    directory = os.path.join(os.getcwd(), "assets/lottie")
    return send_from_directory(directory, "failure.json")

@server.route("/success", methods=['GET'])
def serving_lottie_success():
    directory = os.path.join(os.getcwd(), "assets/lottie")
    return send_from_directory(directory, "success.json")

if __name__ == '__main__':
    # app.run_server(debug=True, dev_tools_props_check=False) # debug mode
    pid = os.fork()
    if pid != 0:
        app.run_server()
    else:
        url = "http://127.0.0.1:8050/"
        webbrowser.open(url)