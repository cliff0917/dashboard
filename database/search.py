import pandas as pd

# 找到 selected_fields 中所有欄位非空的 row
def drop_null(database, selected_fields):
    query = {}
    for key in selected_fields:
        query[key] = {"$exists": True}

    df = pd.json_normalize(database.find(query, {'_id':0}))
    return df