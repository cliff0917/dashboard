import dash_bootstrap_components as dbc
from dash import html

from components import table, graph

# components
table = table.table
graph = graph.graph

show_data = dbc.Col(
    [
        graph,
        html.Br(),
        table,
    ],
    id='show_data',
)