import os
import dash
import webbrowser
import plotly.express as px
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

img_path = './assets/img'
logo = '{}/logo.png'.format(img_path)
btn_sidebar = '{}/btn_sidebar.png'.format(img_path)

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=logo, height="50px", style={'background-color':'white'}) ),
                    dbc.Col(dbc.NavbarBrand("NCKU", className = "ml-2", style={'fontSize': 30})),
                ],
            ),
            href="https://www.ncku.edu.tw/",
            #style={"textDecoration": "none"},
        ),
        
    ],
    color="dark",
    dark=True,
)
SIDEBAR_STYLE={
    "position": "fixed",
    "top": 127.5,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "#f8f9fa",
}

SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 127.5,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "17rem",
    "margin-right": "1rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    'fontSize': 40,
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "1rem",
    "margin-right": "1rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    'fontSize': 40,
}

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
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
    id="sidebar",
    style=SIDEBAR_STYLE,
)
url = dcc.Location(id="url")

menu_bar = html.Div(
    [
        dbc.Row(
            [
                html.Img(src=btn_sidebar, width=50, id='btn_Sidebar'),
                html.P(id='test', style={'margin-top':'13px', 'margin-left':'10px', 'fontSize':17}),
            ],
            style={"margin-left": "6px"},
        ),
    ],
    id="menu_bar",
    style={"background-color":"#f8f9fa", 'border':'1px black solid'}
    )

content = html.Div(
    id="page-content",
    style=CONTENT_STYLE,
)

app.layout = html.Div(
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
@app.callback(
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
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, cur_nclick

all_pages = ['/Home','/Discover','/Security-Events']

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [
        [Output(f"page-{i}-link", "active") for i in range(1, 4)],
        Output('test', 'children')
    ],
    [
        Input("url", "pathname"),
    ],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return [True, False, False], pathname
    return [pathname == page for page in all_pages], pathname

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/Home"]:
        return html.P("歡迎來到首頁")

    elif pathname == "/Discover":
        return html.P("This is the content of page 2. Yay!")

    elif pathname == "/Security-Events":
        return html.P("Oh cool, this is page 3!")

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"此網頁不存在..."),
        ]
    )

if __name__ == '__main__':
    app.run_server(debug=True)
    '''pid = os.fork()
    if pid != 0:
        app.run_server()
    else:
        url = "http://127.0.0.1:8050/"
        webbrowser.open(url)'''
