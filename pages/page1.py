import os
import dash
import webbrowser
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, callback, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL

from statics import get_statics

app = dash.Dash(__name__, suppress_callback_exceptions=True)

img_path = './assets/img'
logo = f'{img_path}/logo.png'
btn_sidebar = f'{img_path}/btn_sidebar.png'
btn_field = f'{img_path}/btn_field.png'
url = dcc.Location(id="url")

global all_fields
df = pd.read_csv('test.csv')
all_fields = list(df.columns)

# 新增 field, btn
add_collapse_combines = []
del_collapse_combines = []
field_style = {'margin-top':'7px', 'margin-left':'50px', "width": 120}
add_btn_style = {'color':'green', 'fontSize':10,'margin-top':'4.98px', 'margin-bottom':'5px', 'align':'center', "width": 50}
del_btn_style = {'color':'red', 'fontSize':10,'margin-top':'4.98px', 'margin-bottom':'5px', 'align':'center', "width": 50}

for i in range(len(all_fields)):
    # 新增 add collapsed fields, btns
    field = all_fields[i]
    add_collapse_field = dbc.Collapse(
        html.P(field, style=field_style),
        id=f"add_collapse_fields_{i}",
        is_open=True,
    )
    add_collapse_btn = dbc.Collapse(
        html.Button('+ add', id=f'add_btn_{i}', style=add_btn_style, n_clicks=0),
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


navbar = dbc.Navbar(
    [
        html.A(
            # 利用 row, col 來控制排版
            dbc.Row(
                [
                    dbc.Col(html.Img(src=logo, height="50px", style={'background-color':'white'})),
                    dbc.Col(dbc.NavbarBrand("NCKU", className = "ml-2", style={'fontSize': 30})),
                ],
            ),
            href="https://www.ncku.edu.tw/",
        )
    ],
    color="dark",
    dark=True,
    sticky='top',
)

SIDEBAR_STYLE={
    "position": "fixed",
    "top": 127.5,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 0,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "orange",
    #"background-color": "#f8f9fa",
    'border':'1px black solid',
}

SIDEBAR_HIDDEN = {
    "position": "fixed",
    "top": 127.5,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 0,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "orange",
    #"background-color": "#f8f9fa",
    'border':'1px black solid',
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-top": 55,
    "margin-left": "18rem",
    "margin-right": "1rem",
    "padding": "2rem 1rem",
    "background-color": "yellow",
    'fontSize': 10,
    #'width': 284,
    'width': 300,
    "maxHeight": "1041px",
    'zIndex':1,
    'border':'1px black solid',
    "overflow": "scroll",
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-top": 55,
    "margin-left": "2rem",
    "margin-right": "1rem",
    "padding": "2rem 1rem",
    "background-color": "yellow",
    'fontSize': 10,
    #'width':284,
    'width': 300,
    "maxHeight": "650px",
    'zIndex':1,
    'border':'1px black solid',
    "overflow": "scroll",
}

CONTENT2_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": 2,
    "margin-top": 55,
    "margin-right": "1rem",
    "padding": "1rem 1rem",
    "background-color": "red",
    'fontSize': 10,
    'zIndex':1,
    'border':'1px black solid',
    'width': '900px', 
}

sidebar = html.Div(
    dbc.Col(
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
    ),
    id="sidebar",
    style=SIDEBAR_STYLE,
)

menu_bar = html.Div(
    [
        dbc.Row(
            [
                html.Img(src=btn_sidebar, width=50, id='btn_Sidebar'),
                html.P(id='path', style={'margin-top':'13px', 'margin-left':'10px', 'fontSize':17}),
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

global table, graph
table = dash_table.DataTable(
    columns=[{'name': column, 'id': column} for column in df.columns],
    data=df.to_dict('records'),
    virtualization=True,
    style_cell={'textAlign': 'left'},
    sort_action='custom',
    sort_mode='multi',
    #filter_action="native",
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 248, 248)',
        }
    ],
    style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'color': 'black',
        'fontWeight': 'bold',
        'textAlign': 'left',
        'border':'1px black solid',
    },
    #fixed_rows={'headers': True},
    id='table',
)

bar_chart = get_statics(df)

graph = dcc.Graph(
    figure=bar_chart,
    id='graph', clickData=None, hoverData=None,
    config={
        'staticPlot': False,     # True, False
        'scrollZoom': True,      # True, False
        'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
        'showTips': False,       # True, False
        'displayModeBar': True,  # True, False, 'hover'
        'watermark': True,
        'modeBarButtonsToRemove': ['pan2d','select2d'],
    },
    style={'width':900, 'border':'1px black solid', 'zIndex':5, "frameMargins": 55,},
)

content2 = dbc.Col(
    [
        graph,
        html.Br(),
        table,
    ],
    id='content2',
    style=CONTENT2_STYLE,
)

all_content = html.Div(
    [
        dbc.Row(
            [
                content,
                content2
            ]
        )
    ],
    style={'width':'100%'}
)

# 網頁 layout
layout = html.Div(
    [
        dcc.Store(id='side_click'),
        url,
        navbar,
        menu_bar,
        sidebar,
        all_content,
        # content,
        # content2,
    ],
    style={'width':'100%'}
)

# 當 btn_sidebar 觸發時, sidebar 和 content 的位置會發生改變
@callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
        #Output("content2", "children"),
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

    return sidebar_style, content_style, cur_nclick#, CONTENT2_STYLE


all_pages = ['/Home','/Discover','/Security-Events']

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
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


FIELDS_HIDDEN_STYLE = {
    "left": "-10rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    #"z-index": 1,
    "overflow-x": "hidden",
    #"transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "#f8f9fa",
}


@callback(
    Output("page-content", "children"),
    [
        Input("url", "pathname"),
        Input("page-content", "children"),
    ]
)
def render_page_content(pathname, children):
    if pathname in ["/", "/Home"]:
        fields_bar = dbc.Col(
            [
                dbc.Row(
                    [
                        dbc.Col(style={"width": 50}),
                        dbc.Button('Enter', id='submit_fields')
                        #html.Img(src=btn_field, width=50, id='btn_field')
                    ],
                ),
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                html.B('Selected fields:', style={'fontSize':20})      
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
                                html.B('Available fields:', style={'fontSize':20})
                            ],
                        ),
                        dbc.Row(
                            [
                                add_collapse_combine for add_collapse_combine in add_collapse_combines
                            ],
                        ),
                    ],
                ),
            ],
            id='fields_bar',
        ),

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

#------------------------------------------
#   Fields 新增, 刪除 按鈕的觸發事件
#   data_table 的更新
#------------------------------------------

# add_btn 觸發事件 => {add_btn, add_fields} 將消失, {del_btn, del_fields} 將出現
# del_btn 觸發事件 => {add_btn, add_fields} 將出現, {del_btn, del_fields} 將消失
global selected_fields, add_next_click
selected_fields = []
add_next_click = [1 for i in range(len(all_fields))]

def click_btn(add_clicks, del_clicks, btn_name):
    global add_next_click, selected_fields, all_fields

    # 監聽 add_btn 是否被按, 若有則新增該 field
    field_idx = int(btn_name)
    if add_clicks == add_next_click[field_idx]:
        add_next_click[field_idx] += 1
        selected_fields.append(all_fields[field_idx])
        print(selected_fields)

        # 顯示 table
        table = dash_table.DataTable(
            columns=[{'name': column, 'id': column} for column in selected_fields],
            data=df.to_dict('records'),
            virtualization=True,
        )
        return [False, False,True, True]

    # add_btn 沒被按 => 則為 del_btn 被按, 或者add_btn, del_btn都沒被按(網頁初始狀態)
    else: 
        try:
            selected_fields.remove(all_fields[field_idx])
            print(selected_fields)
        except:
            pass
        return [True, True, False, False]

# decorator 修飾 click_btn
for i in range(len(all_fields)):
    callback(
        [
            Output(f'add_collapse_fields_{i}', 'is_open'),
            Output(f'{i}', 'is_open'),
            Output(f'del_collapse_fields_{i}', 'is_open'),
            Output(f'del_{i}', 'is_open'),
        ],
        [
            Input(f'add_btn_{i}', 'n_clicks'),
            Input(f'del_btn_{i}', 'n_clicks'),
            Input(f'{i}', 'id'),
        ]
    )(click_btn)

@callback(
    Output('content2', 'children'),
    Input('submit_fields', 'n_clicks'),
)
def update_table(n_clicks):
    global table, graph
    if n_clicks:
        # 如果沒有 field 被選取, 則顯示所有 fields
        if selected_fields == []:
            return [graph, table]

        # 若有 field 被選取, 顯示 new table
        new_table = dash_table.DataTable(
            columns=[{'name': column, 'id': column} for column in selected_fields],
            data=df.to_dict('records'),
            virtualization=True,
            style_cell={'textAlign': 'left'},
            sort_action='custom',
            sort_mode='multi',
            filter_action="native",
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                }
            ],
            style_header={
                'backgroundColor': 'rgb(210, 210, 210)',
                'color': 'black',
                'fontWeight': 'bold',
                'textAlign': 'left',
            },
            id='table',
        )
        return [graph, new_table]
    return dash.no_update
