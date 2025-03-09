from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client.get_database()

user_collection = db.get_collection('users')

def create_user(data):
    user_collection.insert_one(data)

def get_user(user_id):
    return user_collection.find_one({"_id": user_id})
