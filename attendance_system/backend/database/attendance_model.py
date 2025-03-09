from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client.get_database()

attendance_collection = db.get_collection('attendance')

def mark_attendance(data):
    attendance_collection.insert_one(data)

def get_attendance(student_id):
    return attendance_collection.find({"student_id": student_id})
