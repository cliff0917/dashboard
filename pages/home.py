from dash import html

from components import fields

layout = html.Div(
    html.P('歡迎來到首頁!', style=fields.OTHER_FIELD_STYLE),
)