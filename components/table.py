from dash import dash_table

from components import graph

table = dash_table.DataTable(

    virtualization=True,
    style_cell={'textAlign': 'left', 'maxWidth': 135},
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
        'minWidth': '100%',
    },
    id='table',
)