import dash_bootstrap_components as dbc
from dash import html

from components import table, graph

# components
table = table.table
bar_chart = graph.bar_chart

show_data = dbc.Col(
    [
        bar_chart,
        html.Br(),
        table,
    ],
    id='show_data',
)