import dash
from dash import dcc, html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL

from pages import page1#, page2
from components import collapse_item, navbar, sidebar, fields, menubar, table, graph, showData

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# components
navbar = navbar.navbar
menu_bar = menubar.menu_bar
show_data = showData.show_data
url = dcc.Location(id="url")

content = html.Div(
    id='content',
)

layout = html.Div(
    [
        dcc.Store(id='side_click'),
        url,
        navbar,
        menu_bar,
        content,
    ],
)

app.layout = layout

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