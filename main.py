import warnings

warnings.filterwarnings("ignore", category=Warning)

import os
import dash
import webbrowser
import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output

import globals
from database import create_db
from components import navbar, menubar, showData
from pages import home, discover, security_events, nonExist

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# components
navbar = navbar.navbar
menu_bar = menubar.menu_bar
show_data = showData.show_data
url = dcc.Location(id="url")
content = html.Div(id='content')

def serve_layout():
    # 得到最新狀態的 db
    globals.initialize()

    layout = html.Div(
        [
            dcc.Store(id='side_click'),
            url,
            navbar,
            menu_bar,
            content,
        ],
    )
    return layout

# live update, 請注意這裡是要用 serve_layout 而非 serve_layout()
app.layout = serve_layout

# 透過 url 來決定顯示哪個 page
@callback(
    Output('content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname in ['/', '/Home']:
        return home.layout

    elif pathname == '/Discover':
        return discover.layout

    elif pathname == '/Security-Events':
        return security_events.layout
    
    return nonExist.layout  # 若非以上路徑, 則 return 404 message

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_props_check=False)
    """ pid = os.fork()
    if pid != 0:
        app.run_server(dev_tools_props_check=False)
    else:
        url = "http://127.0.0.1:8050/"
        webbrowser.open(url) """