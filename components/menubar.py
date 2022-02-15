from dash import html
import dash_bootstrap_components as dbc

img_path = './assets/img'
btn_sidebar = f'{img_path}/btn_sidebar.png'

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