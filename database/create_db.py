import os
import json
import glob
import pandas as pd
from pymongo import MongoClient

def createDB(database, dir_path, sudoPassword):

    # 更改目錄存取權限
    changePermission_cmd = f"echo {sudoPassword} | sudo -S chmod 777 -R {dir_path}"
    os.system(changePermission_cmd)

    # unzip all .json.gz files
    unzip_cmd = f"echo {sudoPassword} | sudo -S find {dir_path} -iname '*.json.gz' | xargs gunzip"
    os.system(unzip_cmd)
    

    # 找出年份(2000~2099)的資料夾, 並由小到大排序
    targetPattern = "20[0-9][0-9]"
    years = sorted(glob.glob(f'{dir_path}/{targetPattern}'))
    print(years)
    months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
    ]
    month_dict = {}
    for i in range(len(months)):
        month_dict[months[i]] = i + 1

    num = 0
    data = []
    for year_ in years:
        # 按照月份存取
        for month in months:
            try:
                print(f'{year_}/{month}')
                json_files = sorted(glob.glob(f'{year_}/{month}/*.json'))  # 找出所有日期的 .json files, 並由小到大排序
            except: 
                continue
            
            for json_file in json_files:
                f = open(json_file, 'r')
                lines = f.readlines()
                num += len(lines)
                try:
                    json_lines = [json.loads(line) for line in lines]
                except: 
                    pass
                data += json_lines
                print(f'{json_file} 有 {len(lines)} 筆資料')

            month = month_dict[month]
            year = year_.split('/')[-1]
            try:
                database.insert_many(data) # insert data into mongoDB
                print(f'* {year}年{month}月 {num} 筆')
            except:
                pass

    print(f'總共 {num} 筆')