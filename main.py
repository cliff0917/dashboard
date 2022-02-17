import warnings

warnings.filterwarnings("ignore", category=Warning)

import dash
import dash_bootstrap_components as dbc
from pymongo import MongoClient
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State, ALL

from pages import page1#, page2

from database import create_db
from components import collapse_item, navbar, sidebar, fields, menubar, table, graph, showData

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# 需要 sudo 密碼以存取檔案
sudoPassword = 'uscc' # 0
dir_path = '.'  # /var/ossec/logs/alerts

# components
navbar = navbar.navbar
menu_bar = menubar.menu_bar
show_data = showData.show_data
url = dcc.Location(id="url")

content = html.Div(
    id='content',
)

def serve_layout():

    # 建立 mongoDB
    client = MongoClient()
    client.drop_database('pythondb')
    db = client['pythondb']
    current_db = db.list_collection_names(include_system_collections=False)
    posts = db.posts

    if current_db == []:
        create_db.createDB(posts, dir_path, sudoPassword)

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

app.layout = serve_layout

@callback(
    Output('content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname in ['/', '/Home']:
        return html.Div(
            html.P('歡迎來到首頁!', style=fields.OTHER_FIELD_STYLE),
        )

    elif pathname == '/Discover':
        return page1.layout

    elif pathname == '/Security-Events':
        return html.Div(
            html.P('404', style=fields.OTHER_FIELD_STYLE),
        )
    
    # 若非以上路徑, 則 return 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"此網頁不存在..."),
        ]
    )

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_props_check=False)
    """ pid = os.fork()
    if pid != 0:
        app.run_server()
    else:
        url = "http://127.0.0.1:8050/"
        webbrowser.open(url) """