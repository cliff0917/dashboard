import warnings

warnings.filterwarnings("ignore", category=Warning)

import dash
import dash_bootstrap_components as dbc
from pymongo import MongoClient
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State, ALL

from pages import home, discover, security_events, nonExist

import globals
from database import create_db
from components import collapse_item, navbar, sidebar, fields, menubar, table, graph, showData

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
    
    # 若非以上路徑, 則 return 404 message
    return nonExist.layout

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_props_check=False)