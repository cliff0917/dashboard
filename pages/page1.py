import dash
from dash import dcc, html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL

from components import collapse_item, navbar, sidebar, fields, menubar, table, graph, showData

app = dash.Dash(__name__, suppress_callback_exceptions=True)

url = dcc.Location(id="url")
all_pages = ['/Home','/Discover','/Security-Events']

# styles
SIDEBAR_STYLE = sidebar.SIDEBAR_STYLE
SIDEBAR_HIDDEN = sidebar.SIDEBAR_HIDDEN
FIELD_STYLE = fields.FIELD_STYLE
FIELD_STYLE1 = fields.FIELD_STYLE1

# components
navbar = navbar.navbar
sidebar = sidebar.sidebar
menu_bar = menubar.menu_bar
show_data = showData.show_data

field = html.Div(
    id="page-content",
)

content = html.Div(
    [
        dbc.Row(
            [
                field,
                show_data,
            ],
        )
    ],
    id='content',
)

# 網頁 layout
layout = html.Div(
    [
        dcc.Store(id='side_click'),
        url,
        navbar,
        menu_bar,
        sidebar,
        content,
    ],
)


# 當 btn_sidebar 觸發時, sidebar 和 content 的位置會發生改變
@callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],
    [Input("btn_Sidebar", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)
def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDDEN
            field_style = FIELD_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            field_style = FIELD_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        field_style = FIELD_STYLE
        cur_nclick = 'SHOW'

    return sidebar_style, field_style, cur_nclick


# 根據 nav-link 決定網址
@callback(
    [
        [Output(f"page-{i}-link", "active") for i in range(1, 4)],
        Output('path', 'children'),
    ],
    [
        Input("url", "pathname"),
    ],
)
def toggle_active_links(pathname):
    print(pathname)
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return [True, False, False], pathname
    return [pathname == page for page in all_pages], pathname


# 根據網址顯示內容
@callback(
    Output("page-content", "children"),
    [
        Input("url", "pathname"),
        Input("page-content", "children"),
    ]
)
def render_page_content(pathname, children):
    if pathname in ["/", "/Home"]:
        fields_bar = fields.fields_bar
        return fields_bar #html.P("歡迎來到首頁")

    elif pathname == "/Discover":
        content = html.Div(
            html.P("Discover Page"),
        )
        return content

    elif pathname == "/Security-Events":
        return html.P("Security-Events Page")

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"此網頁不存在..."),
        ]
    )