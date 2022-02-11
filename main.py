import os
import dash
import webbrowser
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL

app = dash.Dash(__name__, suppress_callback_exceptions=True)

img_path = './assets/img'
logo = '{}/logo.png'.format(img_path)
btn_sidebar = '{}/btn_sidebar.png'.format(img_path)
url = dcc.Location(id="url")

df = pd.read_csv('test.csv')
all_fields = list(df.columns)

global selected_fields
selected_fields = []

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
        ),
        
    ],
    color="dark",
    dark=True,
    sticky='top'
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
    "margin-top": 55,
    "margin-left": "17rem",
    "margin-right": "1rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    'fontSize': 10,
    'width':284,
    'zIndex':1,
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-top": 55,
    "margin-left": "1rem",
    "margin-right": "1rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    'fontSize': 10,
    'width':284,
    'zIndex':1,
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
    style={"background-color":"#f8f9fa", 'border':'1px black solid', 'position':'fixed',  'width':'100%', 'zIndex':2},
)

content = html.Div(
    id="page-content",
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


# 新增 field, btn
add_collapse_combines = []
del_collapse_combines = []
field_style = {'margin-top':'7px', 'margin-left':'50px', "width": 120}
add_btn_style = {'fontSize':10,'margin-top':'4.98px', 'color':'green','margin-bottom':'5px', 'align':'center', "width": 50}
del_btn_style = {'fontSize':10,'margin-top':'4.98px', 'color':'red','margin-bottom':'5px', 'align':'center', "width": 50}

for i in range(len(all_fields)):
    # 新增 add collapsed fields, btns
    field = all_fields[i]
    add_collapse_field = dbc.Collapse(
        html.P(field, style=field_style),
        id=f"add_collapse_fields_{i}",
        is_open=True,
    )
    add_collapse_btn = dbc.Collapse(
        html.Button('+ add', id=f'add_btn_{i}', style=add_btn_style),
        id=f"{i}",
        is_open=True,
    )
    add_collapse_combine = dbc.Row(
        [
            add_collapse_field, 
            dbc.Col(style={"width": 70}),
            add_collapse_btn,
        ]
    )
    add_collapse_combines.append(add_collapse_combine)

    # 新增 del collapsed fields, btns
    del_collapse_field = dbc.Collapse(
        html.P(field, style=field_style),
        id=f"del_collapse_fields_{i}",
        is_open=False,
    )
    del_collapse_btn = dbc.Collapse(
        html.Button('- del', id=f'del_btn_{i}', style=del_btn_style),
        id=f"del_{i}",
        is_open=False,
    )
    del_collapse_combine = dbc.Row(
        [
            del_collapse_field, 
            dbc.Col(style={"width": 70}),
            del_collapse_btn,
        ]
    )
    del_collapse_combines.append(del_collapse_combine)


@app.callback(
    Output("page-content", "children"), 
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname in ["/", "/Home"]:
        fields_bar = html.Div(
            [
                dbc.Row(
                    [
                        html.B('Selected fields:', style={'fontSize':20, 'margin-left':'6px'})      
                    ],
                ),
                dbc.Row(
                    [
                        del_collapse_combine for del_collapse_combine in del_collapse_combines
                    ],
                ),
                html.Hr(style={'borderColor':'black'}),
                dbc.Row(
                    [
                        html.B('Available fields:', style={'fontSize':20, 'margin-left':'6px'})
                    ],
                ),
                dbc.Row(
                    [
                        add_collapse_combine for add_collapse_combine in add_collapse_combines
                    ],
                ),
            ],
        )
        return fields_bar #html.P("歡迎來到首頁")

    elif pathname == "/Discover":
        content = html.Div(
            html.P("This is the content of page 2. Yay!"),
            #style=DISCOVER_CONTENT_STYLE
        )
        return content

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


# add_btn 觸發事件 => {add_btn, add_fields} 將消失, {del_btn, del_fields} 將出現
# del_btn 觸發事件 => {add_btn, add_fields} 將出現, {del_btn, del_fields} 將消失
global add_next_click
add_next_click = [1 for i in range(len(all_fields))]

def click_btn(add_clicks, del_clicks, btn_name):
    global add_next_click, selected_fields

    # 監聽 add_btn 是否被按, 若有則新增該 field
    if add_clicks == add_next_click[int(btn_name)]:
        add_next_click[int(btn_name)] += 1
        selected_fields.append(btn_name)
        print(selected_fields)
        return [False, False,True, True]

    # add_btn 沒被按 => 則為 del_btn 被按, 或者add_btn, del_btn都沒被按(網頁初始狀態)
    else: 
        try:
            selected_fields.remove(btn_name)
            print(selected_fields)
        except:
            pass
        return [True, True, False, False]

# decorator 修飾 click_btn
for i in range(len(all_fields)):
    app.callback(
        [
            Output(f'add_collapse_fields_{i}', 'is_open'),
            Output(f'{i}', 'is_open'),
            #Output(f'add_collapse_combine_{i}', 'is_open'),
            Output(f'del_collapse_fields_{i}', 'is_open'),
            Output(f'del_{i}', 'is_open'),
        ],
        [
            Input(f'add_btn_{i}', 'n_clicks'),
            Input(f'del_btn_{i}', 'n_clicks'),
            Input(f'{i}', 'id'),
        ]
    )(click_btn)


if __name__ == '__main__':
    app.run_server(debug=True)
    """ pid = os.fork()
    if pid != 0:
        app.run_server()
    else:
        url = "http://127.0.0.1:8050/"
        webbrowser.open(url) """