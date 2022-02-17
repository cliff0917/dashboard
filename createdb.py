import os
import json
import glob
import pandas as pd
from pymongo import MongoClient

sudoPassword = 'uscc'

# 建立 mongoDB
client = MongoClient()
db = client['pythondb']
posts = db.posts

# 找出年份(2000~2099)的資料夾
dir_path = '.'
targetPattern = "20[0-9][0-9]"
years = glob.glob(f'{dir_path}/{targetPattern}')

for year in years:
    year_months = glob.glob(f'{year}/*')
    for year_month in year_months:
        date_files = glob.glob(f'{year_month}/*.json.gz')

        # unzip json.gz files
        for date_file in date_files:
            cmd = f'echo {sudoPassword} | sudo -S gunzip {date_file}'
            os.system(cmd)

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
        posts.insert_many(data) # write to mongoDB