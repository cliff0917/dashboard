from dash import html
import dash_bootstrap_components as dbc

img_path = './assets/img'
logo = f'{img_path}/logo.png'
github = f'{img_path}/github.png'

navbar = dbc.Navbar(
    [
        html.A(
            # 利用 row, col 來控制排版
            dbc.Row(
                [
                    dbc.Col(html.Img(src=logo, height="50px"))
                ],
            ),
            href="https://www.ncku.edu.tw/",
        ),
        dbc.Col(style={'width': 4}),
        html.A(
            # 利用 row, col 來控制排版
            dbc.Row(
                dbc.Col(html.Img(className="github", src=github, height="50px")),
            ),
            href="https://github.com/cliff0917/dashboard",
        ),
    ],
    color="#8EA0A5",
    dark=True,
    sticky='top',
    style={'width':'100%', 'height':'80px'},
)