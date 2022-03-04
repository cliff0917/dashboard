import pandas as pd
import plotly.express as px

from database import get_db
from process_time import process_time

def update(startDate, endDate, col_name, freqs):
    interval_title = process_time.interval_title
    drop_null = {col_name:{"$exists": True}}
    display_cols = {'_id':0, col_name:1}

    # connect to database
    posts = get_db.connect_db()

    # get the set of col_values
    values = posts.distinct('rule.level')

    intervals = list(pd.date_range(startDate, endDate, freq=freqs))
    intervals = process_time.timestamp_format(intervals, endDate) # 轉成 timestamp 格式

    cnt = [[] for i in range(len(values))]
    dic = {values[i]:i for i in range(len(values))}
    
    for i in range(1, len(intervals[:-1])):
        for value in values:
            result = posts.count_documents({'$and':[{'timestamp':{"$gte":intervals[i-1]}}, 
                                                    {'timestamp':{"$lt":intervals[i]}}, 
                                                    {col_name:value}]})
            cnt[dic[value]].append(result)

    for value in values:
        result = posts.count_documents({'$and':[{'timestamp':{"$gt":intervals[-2]}}, 
                                                {'timestamp':{"$lte":intervals[-1]}}, 
                                                {col_name:value}]})
        cnt[dic[value]].append(result)

    data = {'time':intervals[:-1]}
    for i in range(len(values)):
        data[values[i]] = cnt[i]
    df = pd.DataFrame(data)

    fig=px.area(df, x="time", y=values, title="<b>Alert level evolution</b>", 
              labels={"time":f"<b>timestamp per {interval_title[freqs]}</b>", "value": "<b>Count</b>", "variable": col_name},
              hover_data={"time":False}
        )
    fig.update_layout(hovermode="x unified")
    return fig