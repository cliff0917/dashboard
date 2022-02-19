import pandas as pd
import plotly.express as px
from pymongo import MongoClient

def get_statics(df):

    # 無符合條件的資料
    if len(df) == 0:
        return 
    

    time = df['timestamp'].iloc[0]
    date = time.split('T')[0]
    hours = [str(i).zfill(2) for i in range(0, 24)]
    minutes = ['00', '30']

    intervals = []
    for hour in hours:
        for minute in minutes:
            intervals.append(f'{date}T{hour}:{minute}:00.000+0800')

    cnt = []
    for i in range(1, len(intervals)):
        mask1 = df['timestamp'] > intervals[i-1]
        mask2 = df['timestamp'] < intervals[i]
        result = df[mask1 & mask2]
        cnt.append(len(result))

    fig = px.bar(x=intervals[:-1], y=cnt, labels={'x': 'Time', 'y':'Count'})
    return fig