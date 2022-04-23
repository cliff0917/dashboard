import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import html, callback

import globals

# connect to database
globals.initialize()
posts = globals.posts

data = posts.find({}, {'_id':0})
df = pd.json_normalize(data)
all_fields = list(df.columns)
all_fields.remove('timestamp')

# 新增 fields_btn
add_collapse_combines = []
del_collapse_combines = []
field_style = {'margin-top':'7px', 'margin-left':'50px',"width": 150}
add_btn_style = {'color':'green', 'fontSize':10,'margin-top':'4.98px', 'margin-bottom':'5px', 'align':'center', "width": 50}
del_btn_style = {'color':'red', 'fontSize':10,'margin-top':'4.98px', 'margin-bottom':'5px', 'align':'center', "width": 50}

for i in range(len(all_fields)):
    # 新增 add collapsed fields, btns
    field = all_fields[i]
    add_collapse_field = dbc.Collapse(
        html.P(field, style=field_style),
        id=f"add_collapse_fields_{i}",
        is_open=True,
    )
    add_collapse_btn = dbc.Collapse(
        html.Button('+ add', id=f'add_btn_{i}', style=add_btn_style, n_clicks=0),
        id=f"{i}",
        is_open=True,
    )
    add_collapse_combine = dbc.Row(
        [
            add_collapse_field,
            dbc.Col(style={"width": 70}),
            add_collapse_btn,
        ]
    )

    add_collapse_combines.append(add_collapse_combine)

    # 新增 del collapsed fields, btns
    del_collapse_field = dbc.Collapse(
        html.P(field, style=field_style),
        id=f"del_collapse_fields_{i}",
        is_open=False,
    )
    del_collapse_btn = dbc.Collapse(
        html.Button('- del', id=f'del_btn_{i}', style=del_btn_style),
        id=f"del_{i}",
        is_open=False,
    )
    del_collapse_combine = dbc.Row(
        [
            del_collapse_field,
            dbc.Col(style={"width": 70}),
            del_collapse_btn,
        ]
    )

    del_collapse_combines.append(del_collapse_combine)

#------------------------------------------
#   Fields 新增, 刪除 按鈕的觸發事件
#------------------------------------------
global selected_fields, add_next_click
selected_fields = []
add_next_click = [1 for i in range(len(all_fields))]

def click_btn(add_clicks, del_clicks, btn_name):
    global add_next_click, selected_fields, all_fields

    # 監聽 add_btn 是否被按, 若有則新增該 field
    field_idx = int(btn_name)
    if add_clicks == add_next_click[field_idx]:
        add_next_click[field_idx] += 1
        field_name = all_fields[field_idx]
        selected_fields.append(field_name)
        # print(selected_fields)
        return [False, False,True, True]

    # add_btn 沒被按 => 則為 del_btn 被按, 或者add_btn, del_btn都沒被按(網頁初始狀態)
    else:
        try:
            selected_fields.remove(all_fields[field_idx])
            # print(selected_fields)
        except:
            pass
        return [True, True, False, False]

# decorator 修飾 click_btn
for i in range(len(all_fields)):
    callback(
        [
            Output(f'add_collapse_fields_{i}', 'is_open'),
            Output(f'{i}', 'is_open'),
            Output(f'del_collapse_fields_{i}', 'is_open'),
            Output(f'del_{i}', 'is_open'),
        ],
        [
            Input(f'add_btn_{i}', 'n_clicks'),
            Input(f'del_btn_{i}', 'n_clicks'),
            Input(f'{i}', 'id'),
        ],
        prevent_initial_call=True
    )(click_btn)