from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client.get_database()

student_collection = db.get_collection('students')

class Student:
    def __init__(self, student_id, name, student_class):
        self.student_id = student_id
        self.name = name
        self.student_class = student_class

    @staticmethod
    def get_all():
        client = MongoClient('mongodb://localhost:27017/')
        db = client['attendance_db']
        students_collection = db['students']
        students = list(students_collection.find({}, {'_id': 0}))
        client.close()
        return students

def create_student(data):
    student_collection.insert_one(data)

def get_student(student_id):
    return student_collection.find_one({"_id": student_id})
