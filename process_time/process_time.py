import pandas as pd
from datetime import datetime, timedelta

interval_title={'1min': 'minute', '5min': '5 minutes', '10min': '10 minutes','30min': '30 minutes', 
                '1H': 'hour', '3H': '3 hours', '12H': '12 hours', 
                '1D': 'day', '7D': '7 days', '30D': '30days'}

# 修正8小時時差並轉成string
def localTime(time):
    dateFormat = '%Y-%m-%dT%H:%M:%S.%f'
    local = (pd.to_datetime(time) + pd.Timedelta(hours=8)).strftime(dateFormat)
    local = local[:-3] + '+0800'
    return local

# 將 interval 轉成 timestamp 格式
def timestamp_format(intervals, endDate):
    for i in range(len(intervals)):
        intervals[i] = str(intervals[i])
        date, time = intervals[i].split(' ')
        day_time, _ = time.split('+')
        intervals[i] =  date + 'T' + day_time[:-3] + '+0800'

    # 將 endDate 轉成 timestamp 格式, 因為 startDate, endDate 的時間差可能無法被 freq 整除, 故要特殊處理
    # datetime.now 和 dash_datetimepicker 的時間格式不同, try 是特殊處理 datetime.now 的, 因為它中間是用空白隔開
    # 而 datetimepicker 本身就是 timestamp 格式 
    try:
        date, day_time  = endDate.split(' ')
        endDate = date + 'T' + day_time
    except:
        pass

    intervals.append(endDate)
    return intervals

# convert string to datetime format
def string_to_time(time):
    dateFormat = "%Y-%m-%dT%H:%M:%S.%f%z"
    time = datetime.strptime(time, dateFormat)
    return time

def get_freq(startDate, endDate):
    startDate = string_to_time(startDate)
    endDate = string_to_time(endDate)

    days = (endDate-startDate).days
    seconds = (endDate-startDate).seconds
    if days == 0:
        if seconds >= 1*60*60 and seconds < 3*60*60:    # 1 <= x < 3 (hours)
            freqs = '1min'
        elif seconds >= 3*60*60 and seconds < 8*60*60:  # 3 <= x < 8 (hours)
            freqs = '5min'
        elif seconds >= 8*60*60 and seconds < 17*60*60:  # 8 <= x < 17 (hours)
            freqs = '10min'
        elif seconds >= 17*60*60:   # x >= 17 (hours)
            freqs = '30min'
    elif days < 2:  #  17 <= x < 48 (hours)
        freqs = '30min'
    elif days >=2 and days < 5:
        freqs = '1H' 
    elif days >= 5 and days < 12:
        freqs = '3H'
    elif days >= 12 and days < 50:
        freqs = '12H'
    elif days >= 50 and days < 365:
        freqs = '1D'
    elif days >= 365 and days < 3*365:  # 1 <= x < 3 (years)
        freqs = '7D'
    else:  # x > 3 (years)
        freqs = '30D'
    print(freqs)
    return freqs