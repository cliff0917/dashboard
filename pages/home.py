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

def serve_layout():
    layout = html.Div(
        [
            html.P('歡迎來到首頁!'),
            html.Hr(),
            html.Li('使用說明:'),
            html.Ul(
                [
                    html.Ul(
                        [
                            html.Li('1. 按 F5 更新資料庫中的資料'),
                            html.Li('2. DateTime Picker 旁邊的 update 按鈕不更新資料庫的資料, 而是查詢資料庫的資料'),
                            html.Li('3. 滑鼠移到 Graph 上可顯示詳細資訊'),
                            html.Li('4. Graph 可以利用滑鼠縮小放大, 雙擊便可恢復原狀'),
                        ],
                        style={'fontSize': 30}
                    ),
                ]
            ),
            html.Li('Discover Page:'),
            html.Ul(
                [
                    html.Ul(
                        [
                            html.Li('1. 當 selected fields 為空時, 預設顯示所有的 fields; 否則, 顯示 #(第幾筆資料), timestamp, 和 selected fields'),
                            html.Li('2. Table 中欄位名稱旁邊的箭頭可以點選, 選擇資料要升or降冪排序'),
                            html.Ul(
                                [
                                    html.Li(
                                        [
                                            '升冪: 所選欄位的資料由小到大排序 ',
                                            html.Img(src='./assets/img/asc.png'),
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            '降冪: 所選欄位的資料由大到小排序 ',
                                            html.Img(src='./assets/img/desc.png'),
                                        ]
                                    ),
                                ]
                            ),
                            html.Li('3. 滑鼠移到 Table 中, 可以顯示詳細資訊'),
                            html.Img(src='./assets/img/hover.png'),
                        ],
                        style={'fontSize': 30}
                    ),
                ]
            ),
        ],
        style=STYLE,
    )
    return layout