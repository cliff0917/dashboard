import os
from pymongo import MongoClient

client = MongoClient()
db = client['pythondb']
posts = db.posts
client.drop_database('pythondb') # delete db
os.remove('./last_date.pkl')