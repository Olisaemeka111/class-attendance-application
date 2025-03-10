from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client.get_database()

user_collection = db.get_collection('users')

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    @staticmethod
    def create_user(username, password):
        if user_collection.find_one({"username": username}):
            return False
        user_collection.insert_one({
            "username": username,
            "password": generate_password_hash(password)
        })
        return True

    @staticmethod
    def authenticate(username, password):
        user = user_collection.find_one({"username": username})
        if user and check_password_hash(user['password'], password):
            return True
        return False
