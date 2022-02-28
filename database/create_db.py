import os
import json
import glob
import pandas as pd
from pymongo import MongoClient

def createDB(database, dir_path, sudoPassword):

    # 更改目錄存取權限
    changePermission_cmd = f"echo {sudoPassword} | sudo -S chmod 777 -R {dir_path}"
    os.system(changePermission_cmd)

    # unzip all .json.gz files => 用 "find {dir_path} -name '*.json.gz' -exec gunzip {} +" 指令
    # f sting 中用兩個{}, 來顯示{}
    unzip_cmd = f"echo {sudoPassword} | sudo -S find {dir_path} -name '*.json.gz' -exec gunzip {{}} +"
    os.system(unzip_cmd)
    
    # 找出年份(2000~2099)的資料夾, 並由小到大排序
    targetPattern = "20[0-9][0-9]"
    years = sorted(glob.glob(f'{dir_path}/{targetPattern}'))
    
    months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
    ]

    month_dict = {}
    for i in range(len(months)):
        month_dict[months[i]] = i + 1

    num = 0
    data = []
    error_file = ''
    for year_ in years:
        # 按照月份存取
        for month in months:
            try:
                json_files = sorted(glob.glob(f'{year_}/{month}/*.json'))  # 找出所有日期的 .json files, 並由小到大排序
                for json_file in json_files:
                    f = open(json_file, 'r+')
                    lines = f.readlines()
                    try:
                        json_lines = [json.loads(line) for line in lines]
                        num += len(lines)
                    except: 
                        error_file = json_file
                    data += json_lines
                    # print(f'{json_file} 有 {len(lines)} 筆資料')
            except: 
                continue
    try:
        database.insert_many(data) # insert data into mongoDB
    except:
        print(f'重新 insert {error_file}')
        f = open(error_file, 'r')
        lines = f.readlines()
        json_lines = [json.loads(line) for line in lines]
        num += len(lines)
        database.insert_many(json_lines)
    print(f'總共 {num} 筆')