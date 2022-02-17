import os
import json
import glob
import pandas as pd
from pymongo import MongoClient

def createDB(database, sudoPassword):
    # 找出年份(2000~2099)的資料夾
    dir_path = '.'

    # 更改目錄存取權限
    changePermission_cmd = f"echo {sudoPassword} | sudo -S chmod 777 {dir_path}"
    os.system(changePermission_cmd)

    # unzip json.gz files
    unzip_cmd = f"echo {sudoPassword} | sudo -S find {dir_path} -iname '*.json.gz' | xargs gunzip"
    os.system(unzip_cmd)

    targetPattern = "20[0-9][0-9]"
    years = glob.glob(f'{dir_path}/{targetPattern}')

    for year in years:
        year_months = glob.glob(f'{year}/*')
        for year_month in year_months:
            num = 0
            data = []
            json_files = sorted(glob.glob(f'{year_month}/*.json'))  # get json files
            for json_file in json_files:
                f = open(json_file, 'r')
                lines = f.readlines()
                num += len(lines)
                print(f'{json_file} 有 {len(lines)} 筆資料')
                json_lines = [json.loads(line) for line in lines]
                data += json_lines

            print(f'總共 {num} 筆')
            database.insert_many(data) # insert data into mongoDB