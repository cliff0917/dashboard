import json
import pandas as pd
from datetime import datetime, timedelta

# generator
def gen_dates(start, days):
    day = timedelta(days=1)
    for offset in range(days):
        yield start + (day * offset)

def get_date_list(start, end):
    dateFormat = "%Y-%m-%d"
    start = datetime.strptime(start, dateFormat).date()
    end = datetime.strptime(end, dateFormat).date()
    dates = []
    for date in gen_dates(start, (end-start).days+1): # +1 是把 endDate 加進去 lst 中
        dates.append(str(date))
    return dates

def get_time_info(time):
    year, month, day = time.split('-')
    return year, month, day

def update_db(posts, dir_path):
    last = posts.find({}, {'timestamp':1, '_id':0}).limit(1).sort([('$natural',-1)])
    last_time = pd.json_normalize(last)['timestamp'].to_string()
    last_time = last_time.split(' ')[-1]
    last_time = last_time.split('T')[0]

    dateFormat = "%Y-%m-%d %H:%M:%S.%f"
    now = datetime.now()
    now_time = datetime.strftime(now, dateFormat)
    now_time = now_time.split(' ')[0]

    months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
    ]

    convert_month = {}
    for i in range(len(months)):
        convert_month[str(i+1).zfill(2)] = months[i]
        
    dates_lst = get_date_list(last_time, now_time)

    # 上次更新的最後一天之data數目
    last_cnt = posts.count_documents({'timestamp': {"$gte": last_time}})

    # 特殊處理上次更新的最後一天
    data = []
    last_y, last_m, last_d = get_time_info(dates_lst[0])
    f = open(f'{dir_path}/{last_y}/{convert_month[last_m]}/ossec-alerts-{last_d}.json', 'r+')
    lines = f.readlines()
    update_lines = lines[last_cnt:]
    json_lines = [json.loads(line) for line in update_lines]
    data += json_lines
    # print(f'{dates_lst[0]} 新增{len(json_lines)}筆')

    # 更新其他天的資料
    for date in dates_lst[1:]:
        year, month, day = get_time_info(date)
        try:
            f = open(f'{dir_path}/{year}/{convert_month[month]}/ossec-alerts-{day}.json', 'r+')
            lines = f.readlines()
            json_lines = [json.loads(line) for line in lines]
            data += json_lines
        except:
            pass
            # print(f'{date} 沒有資料')
            
    # print('-' * 25)
    if data == []:
        print('沒有要新增的資料')
    else:
        posts.insert_many(data) # insert data into mongoDB
        print(f'新增{len(data)}筆資料')