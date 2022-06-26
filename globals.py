import pandas as pd
from database import get_db

def initialize():
    global posts, num, first, current_db, selected_fields, add_next_click, all_fields, fields_num
    # 需要 sudo 密碼以存取檔案
    sudoPassword = 'uscc' # 0
    dir_path = '.'  # /var/ossec/logs/alerts
    selected_fields = []
    client, posts, num, current_db, = get_db.get_current_db(dir_path, sudoPassword)
    data = posts.find({}, {'_id':0})
    df = pd.json_normalize(data)
    all_fields = list(df.columns)
    all_fields.remove('timestamp')
    fields_num = len(all_fields)
    add_next_click = [1 for i in range(fields_num)]