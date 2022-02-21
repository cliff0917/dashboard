from pymongo import MongoClient

from database import create_db

def connect_db(dir_path, sudoPassword):
    client = MongoClient()
    db = client['pythondb']
    # client.drop_database('pythondb') # delete db
    current_db = db.list_collection_names(include_system_collections=False)
    posts = db.posts
    if current_db == []:
        create_db.createDB(posts, dir_path, sudoPassword)
    return client, posts