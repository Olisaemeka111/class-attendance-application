import sys
import os
import logging
from pymongo import MongoClient, errors  # Import errors from pymongo
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from database.connection import db
from database.student_model import Student
from database.attendance_model import Attendance
from database.user_model import User
from config import Config

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET
jwt = JWTManager(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Connect to MongoDB with error handling
try:
    client = MongoClient(Config.MONGO_URI)
    db = client[Config.MONGO_DB_NAME]
    logger.debug("Connected to MongoDB")
except errors.ConnectionError as e:
    logger.error(f"Could not connect to MongoDB: {e}")
    sys.exit(1)

@app.route('/')
def home():
    logger.debug("Home endpoint called")
    return jsonify({"message": "Attendance System API Running"})

@app.route('/health')
def health():
    logger.debug("Health endpoint called")
    try:
        # Check MongoDB connection
        client.admin.command('ping')
        return jsonify({"status": "healthy"})
    except errors.PyMongoError as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({"status": "unhealthy"}), 500

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    logger.debug(f"Register endpoint called with data: {data}")
    try:
        if User.create_user(data['username'], data['password']):
            return jsonify({"message": "User registered successfully"})
        return jsonify({"error": "User already exists"}), 400
    except Exception as e:
        logger.error(f"Error in register endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    logger.debug(f"Login endpoint called with data: {data}")
    try:
        user = User.authenticate(data['username'], data['password'])
        if user:
            token = create_access_token(identity=data['username'])
            return jsonify({"token": token})
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        logger.error(f"Error in login endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    logger.debug("Get students endpoint called")
    try:
        students = Student.get_all()
        return jsonify(students)
    except Exception as e:
        logger.error(f"Error in get_students endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/attendance', methods=['POST'])
@jwt_required()
def mark_attendance():
    data = request.json
    logger.debug(f"Mark attendance endpoint called with data: {data}")
    try:
        Attendance.mark_attendance(data['student_id'], data['subject'])
        return jsonify({"message": "Attendance marked"})
    except Exception as e:
        logger.error(f"Error in mark_attendance endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    logger.debug("Starting the Flask application")
    app.run(debug=True, host='0.0.0.0')
