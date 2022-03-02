from dash import html

STYLE = {
    "transition": "margin-left .5s",
    "margin-top": 35,
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    'fontSize': 40,
    'zIndex':1,
    'border':'1px black solid',
}

layout = html.Div(
    html.P('歡迎來到首頁!', style=STYLE),
)