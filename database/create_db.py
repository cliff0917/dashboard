import os
import json
import glob
import pandas as pd
from pymongo import MongoClient

def createDB(database, dir_path, sudoPassword):
    dir_path = '.'

    # 更改目錄存取權限
    changePermission_cmd = f"echo {sudoPassword} | sudo -S chmod 777 - R {dir_path}"
    os.system(changePermission_cmd)

    # unzip all .json.gz files
    unzip_cmd = f"echo {sudoPassword} | sudo -S find {dir_path} -iname '*.json.gz' | xargs gunzip"
    os.system(unzip_cmd)

    # 找出年份(2000~2099)的資料夾
    targetPattern = "20[0-9][0-9]"
    years = glob.glob(f'{dir_path}/{targetPattern}')
    month_dec = {
                'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6,
                'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12,
            }

    num = 0
    data = []
    for year_ in years:
        year_months = glob.glob(f'{year_}/*')
        for year_month in year_months:
            #data = []
            json_files = sorted(glob.glob(f'{year_month}/*.json'))  # get json files
            for json_file in json_files:
                f = open(json_file, 'r')
                lines = f.readlines()
                num += len(lines)
                try:
                    json_lines = [json.loads(line) for line in lines]
                except:
                    print('請重試一次')
                data += json_lines
                print(f'{json_file} 有 {len(lines)} 筆資料')

            month = month_dec[year_month.split('/')[-1]]
            year = year_month.split('/')[-2]
            database.insert_many(data) # insert data into mongoDB
            print(f'* {year}年{month}月 {num} 筆')
    print(f'總共 {num} 筆')