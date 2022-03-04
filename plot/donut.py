import plotly.graph_objects as go

from database import get_db

def calculate_cnt(startDate, endDate, col_name):
    # connect to database
    posts = get_db.connect_db()

    # get the set of col_values
    set_values = posts.distinct(col_name)

    cnt = []
    for value in set_values:
        result = posts.count_documents({'$and':[{col_name:{"$in": [value]}}, 
                                                {'timestamp':{"$gte":startDate}}, 
                                                {'timestamp':{"$lte":endDate}}]})
        cnt.append(result)
    return cnt, set_values

def update(startDate, endDate, col_name, title):
    cnt, set_values = calculate_cnt(startDate, endDate, col_name)
    fig = go.Figure(go.Pie(
        name = col_name,
        values = cnt,
        labels = set_values,
        text = set_values,
        hovertemplate = "%{label} <br>出現次數:%{value} <br>佔比: %{percent}",
        hole=0.8,
    ))
    fig.update_layout(title_text=f"<b>{title}</b>")
    return fig