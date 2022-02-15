import dash
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, dash_table
from dash.dependencies import Input, Output, State, ALL

from statics import get_statics
from components import collapse_item, fields, table, graph

df = collapse_item.df
selected_fields = collapse_item.selected_fields
fields = fields.fields_bar
table = table.table
graph = graph.graph

DISPLAY_STYLE = {
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

show_data = dbc.Col(
    [
        html.H3(f'共{len(df)}筆資料', style={'textAlign': 'center'}),
        graph,
        html.Br(),
        table,
    ],
    id='show_data',
    style=DISPLAY_STYLE,
)

@callback(
    Output('show_data', 'children'),
    Input('submit_fields', 'n_clicks'),   
)
def update_table(n_clicks):
    global table, graph
    if n_clicks:
        # 如果沒有 field 被選取, 則顯示所有 fields
        if selected_fields == []:
            dataNum = html.H3(f'共{len(df)}筆資料', style={'textAlign': 'center'})
            return [dataNum, graph, html.Br(), table]

        # 若有 field 被選取, 顯示 new table
        selected_df = df.copy()
        selected_df = selected_df[selected_fields].dropna()

        if len(selected_df) == 0:
            message = html.H3('無符合條件的資料', style={'textAlign': 'center'})
            return [message]

        new_table = dash_table.DataTable(
            columns=[{'name': column, 'id': column} for column in selected_fields],
            data=selected_df.to_dict('records'),
            virtualization=True,
            style_cell={'textAlign': 'left', 'minHeight': '100%'},
            sort_action='custom',
            sort_mode='multi',
            #filter_action="native",
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                }
            ],
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in selected_df.to_dict('records')
            ],
            style_header={
                'backgroundColor': 'rgb(210, 210, 210)',
                'color': 'black',
                'fontWeight': 'bold',
                'textAlign': 'left',
            },
            id='table',
        )

        graph_df = df.copy()
        graph_fields = selected_fields.copy()
        if 'timestamp' not in selected_fields:
            graph_fields = selected_fields.copy()
            graph_fields.insert(0, 'timestamp')
            print(graph_fields)
            graph_df = graph_df[graph_fields].dropna()
        else:
            graph_df = graph_df[selected_fields].dropna()
        bar_chart = get_statics(graph_df)
        dataNum = html.H3(f'共{len(graph_df)}筆資料', style={'textAlign': 'center'})

        new_graph = dcc.Graph(
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
            style={'border':'1px black solid', 'zIndex':5, "frameMargins": 55,},
        )
        return [dataNum, new_graph, html.Br(), new_table]
    return dash.no_update