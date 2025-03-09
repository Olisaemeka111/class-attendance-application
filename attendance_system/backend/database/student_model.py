from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client.get_database()

student_collection = db.get_collection('students')

def create_student(data):
    student_collection.insert_one(data)

def get_student(student_id):
    return student_collection.find_one({"_id": student_id})
