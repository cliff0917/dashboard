from dash import html
import dash_bootstrap_components as dbc

img_path = './assets/img'
logo = f'{img_path}/logo.png'
github=f'{img_path}/github.png'

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
        ),
        dbc.Col(style={'width': 4}),
        html.A(
            # 利用 row, col 來控制排版
            dbc.Row(
                dbc.Col(html.Img(src=github, height="50px", style={'background-color':'white'})),
            ),
            href="https://github.com/cliff0917/dashboard",
        ),
    ],
    color="dark",
    dark=True,
    sticky='top',
    style={'width':'100%'},
)