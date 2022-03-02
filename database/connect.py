from pymongo import MongoClient

from database import create_db, update

def get_current_db(dir_path, sudoPassword):
    client = MongoClient()
    db = client['pythondb']
    # client.drop_database('pythondb') # delete db
    current_db = db.list_collection_names(include_system_collections=False)
    posts = db.posts
    if current_db == []:
        create_db.createDB(posts, dir_path, sudoPassword)
    else:
        update.update_db(posts, dir_path)
    return client, posts

def connect_to_db():
    client = MongoClient()
    db = client['pythondb']
    posts = db.posts
    return posts