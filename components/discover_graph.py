from dash import dcc, html,  dash_table

from plot import bar
from components import collapse_item, se_graph

CONFIG = se_graph.CONFIG
BAR_STYLE = {'border':'1px black solid', 'zIndex':1}

def update_display(startDate, endDate, freqs):
    # 根據 selected_fields 篩選資料
    bar_fig, df = bar.update(startDate, endDate, freqs, collapse_item.selected_fields)

    # 若無資料
    if len(df) == 0:
        return [f'從 {startDate} 到 {endDate}', '此區間無資料', []]

    # 若有資料
    bar_graph = dcc.Graph(
        figure=bar_fig,
        id='bar_chart', clickData=None, hoverData=None,
        config=CONFIG, style=BAR_STYLE,
    )

    # 解決 data table 中 list 的顯示問題, 將 df 中的 list 轉成 string 用逗號隔開, 並串接在一起
    for column in list(df.columns):
        df[column] = [', '.join(map(str, l)) if isinstance (l, list) else l for l in df[column]]

    # 根據 columns 名稱長度, 自動調整 data table 的 header 寬度
    long_column_names = [{"if": {"column_id": column}, "min-width": "300px"} for column in df.columns if len(column) >= 30]
    med_column_names = [{"if": {"column_id": column}, "min-width": "225px"} for column in df.columns if (len(column) > 15 and len(column)) < 30]
    small_column_names = [{"if": {"column_id": column}, "min-width": "120px"} for column in df.columns if len(column) <= 15]

    adjusted_columns = long_column_names + med_column_names + small_column_names

    table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns = [{'name': column, 'id': column} for column in df.columns],
        virtualization=True,
        style_cell={'textAlign': 'left', 'overflow': 'hidden',
                    'textOverflow': 'ellipsis', 'minWidth': 240, 'maxWidth': 240},
        sort_action='custom',
        sort_mode='multi',
        fixed_rows={
            'headers': True,
            'data': 0
        },
        style_cell_conditional=adjusted_columns,
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
        tooltip_data=[
            {
                column: {'value': f'{column}\n\n{value}', 'type': 'markdown'}
                for column, value in row.items()
            } for row in df.to_dict('records')
        ],
        tooltip_header = {i: i for i in df.columns},
    )

    display = [
        bar_graph,
        html.Br(),
        table,
    ]

    return [f'從 {startDate} 到 {endDate}', f'{len(df)} hits', display]