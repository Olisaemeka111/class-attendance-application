from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client.get_database()

attendance_collection = db.get_collection('attendance')

class Attendance:
    def __init__(self, student_id, subject, status):
        self.student_id = student_id
        self.subject = subject
        self.status = status

    @staticmethod
    def mark_attendance(student_id, subject):
        attendance_collection.insert_one({
            "student_id": student_id,
            "subject": subject,
            "status": "present"
        })

    @staticmethod
    def get_attendance(student_id):
        return list(attendance_collection.find({"student_id": student_id}, {'_id': 0}))

def create_attendance(data):
    attendance_collection.insert_one(data)

def get_attendance(student_id):
    return attendance_collection.find_one({"student_id": student_id})
