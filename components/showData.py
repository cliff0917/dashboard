import dash
import pandas as pd
import dash_bootstrap_components as dbc
from pymongo import MongoClient
from dash import dcc, html, callback, dash_table
from dash.dependencies import Input, Output, State, ALL

import globals
from database import search
from statics import get_statics
from components import collapse_item, fields, table, graph, datePicker

# components
global df, selected_fields, fields, table, graph
df = collapse_item.df
selected_fields = collapse_item.selected_fields
fields = fields.fields_bar
table = table.table
graph = graph.graph

show_data = dbc.Col(
    [
        html.H3(f'{len(df)} hits', style={'textAlign': 'center'}),
        graph,
        html.Br(),
        table,
    ],
    id='show_data',
    #style=NEW_DISPLAY_STYLE,
)

@callback(
    Output('show_data', 'children'),
    Input('submit_fields', 'n_clicks'),   
)
def update_table(n_clicks):
    global df, selected_fields, fields, table, graph

    posts = globals.posts
    data = posts.find({}, {'_id':0})
    df = pd.json_normalize(data)

    if n_clicks:
        # 如果沒有 field 被選取, 則顯示所有 fields
        if selected_fields == []:
            dataNum = html.H3(f'{len(df)} hits', style={'textAlign': 'center'})
            return [graph, html.Br(), table]

        # 若有 field 被選取, 顯示 new table
        database = collapse_item.posts
        selected_df = search.drop_null(database, selected_fields)

        # 若無符合的資料
        if len(selected_df) == 0:
            message = html.H3('無符合條件的資料', style={'textAlign': 'center'})
            return [message]

        # 若有符合的資料
        dataNum = html.H3(f'共{len(selected_df)}筆資料', style={'textAlign': 'center'})

        new_table = dash_table.DataTable(
            columns=[{'name': column, 'id': column} for column in selected_fields],
            data=selected_df.to_dict('records'),
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
                'minWidth': '100%'
            },
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in df.to_dict('records')
            ],
        )

        bar_chart = get_statics(selected_df)

        new_graph = dcc.Graph(
            figure=bar_chart,
            id='graph', clickData=None, hoverData=None,
            config={
                'staticPlot': False,     # True, False
                'scrollZoom': True,      # True, False
                'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                'showTips': True,       # True, False
                'displayModeBar': True,  # True, False, 'hover'
                'watermark': True,
                'modeBarButtonsToRemove': ['pan2d','select2d'],
            },
            style={'border':'1px black solid', 'zIndex':1, "frameMargins": 55},
        )
        return [dataNum, new_graph, html.Br(), new_table]
    return dash.no_update