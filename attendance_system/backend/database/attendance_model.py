from pymongo import MongoClient
from config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Use the MONGO_URI from config.py
client = MongoClient(Config.MONGO_URI)
db = client[Config.MONGO_DB_NAME]

attendance_collection = db.get_collection('attendance')

class Attendance:
    def __init__(self, student_id, subject, status):
        self.student_id = student_id
        self.subject = subject
        self.status = status

    @staticmethod
    def mark_attendance(student_id, subject):
        try:
            attendance_collection.insert_one({
                "student_id": student_id,
                "subject": subject,
                "status": "present"
            })
            logger.info(f"Marked attendance for student_id: {student_id}, subject: {subject}")
        except Exception as e:
            logger.error(f"Error marking attendance: {e}")

    @staticmethod
    def get_attendance(student_id):
        try:
            attendance = list(attendance_collection.find({"student_id": student_id}, {'_id': 0}))
            logger.info(f"Retrieved attendance for student_id: {student_id}")
            return attendance
        except Exception as e:
            logger.error(f"Error retrieving attendance: {e}")
            return []

def create_attendance(data):
    try:
        attendance_collection.insert_one(data)
        logger.info(f"Created attendance record: {data}")
    except Exception as e:
        logger.error(f"Error creating attendance record: {e}")

def get_attendance(student_id):
    try:
        attendance = attendance_collection.find_one({"student_id": student_id})
        logger.info(f"Retrieved attendance for student_id: {student_id}")
        return attendance
    except Exception as e:
        logger.error(f"Error retrieving attendance: {e}")
        return None
