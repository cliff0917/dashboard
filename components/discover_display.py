from dash import dcc, html,  dash_table

from plot import bar
from components.se_display import CONFIG
from components.collapse_item import selected_fields, timestamp_auto_insert

global CONFIG
BAR_STYLE = {'border':'1px black solid', 'zIndex':1}

def update(startDate, endDate, freqs):
    global selected_fields, timestamp_auto_insert, CONFIG

    # 若所選 fields 中沒有 timestamp 則自動加入 timestamp 在最前面
    if len(selected_fields) != 0 and 'timestamp' not in selected_fields:
        selected_fields.insert(0, 'timestamp')
        timestamp_auto_insert = 1

    # 若 fields 中只剩下 timestamp, 且 timestamp 是自動 insert 的 => 刪除 timestamp, 讓 fields 為空 (data table 會顯示所有 fields)
    elif selected_fields == ['timestamp'] and timestamp_auto_insert == 1:
        selected_fields.remove('timestamp')
        timestamp_auto_insert = 0

    # 根據 selected_fields 篩選資料(若 fields 為空, table 顯示所有 fields)
    bar_fig, df = bar.update(startDate, endDate, freqs, selected_fields)

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

    # 根據 column 名稱長度, 自動調整 data table 的 header 寬度
    long_column_names = [{"if": {"column_id": column}, "min-width": "300px"} for column in df.columns if len(column) >= 30]
    med_column_names = [{"if": {"column_id": column}, "min-width": "225px"} for column in df.columns if (len(column) > 15 and len(column)) < 30]
    small_column_names = [{"if": {"column_id": column}, "min-width": "120px"} for column in df.columns if len(column) <= 15]

    adjusted_columns = long_column_names + med_column_names + small_column_names

    table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'name': column, 'id': column} for column in df.columns],
        virtualization=True,
        sort_action='custom',
        sort_mode='multi',
        # 要 minWidth, maxWidth 同時設一樣, 再搭配 fixed_rows, 才能 fixed header
        style_cell={
            'textAlign': 'left',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'minWidth': 240,
            'maxWidth': 240,
            'whiteSpace': 'pre-line',   # 超過自動換行
        },
        fixed_rows={
            'headers': True,
            'data': 0,
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
        tooltip_header={i: i for i in df.columns},
        style_table={
            'height': 700,
            'overflowY': 'auto',
        },
        # page_size=100, # 預設一頁有250列
    )

    display = [
        bar_graph,
        html.Br(),
        table,
    ]

    return [f'從 {startDate} 到 {endDate}', f'{len(df)} hits', display]