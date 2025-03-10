import sys
import os
import logging
from pymongo import MongoClient  # Import MongoClient
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
# Update the import paths
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

# Connect to MongoDB
client = MongoClient(Config.MONGO_URI)
db = client[Config.MONGO_DB_NAME]

@app.route('/')
def home():
    app.logger.debug("Home endpoint called")
    return jsonify({"message": "Attendance System API Running"})

@app.route('/health')
def health():
    app.logger.debug("Health endpoint called")
    return jsonify({"status": "healthy"})

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    app.logger.debug(f"Register endpoint called with data: {data}")
    if User.create_user(data['username'], data['password']):
        return jsonify({"message": "User registered successfully"})
    return jsonify({"error": "User already exists"}), 400

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    app.logger.debug(f"Login endpoint called with data: {data}")
    user = User.authenticate(data['username'], data['password'])
    if user:
        token = create_access_token(identity=data['username'])
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    app.logger.debug("Get students endpoint called")
    students = Student.get_all()
    return jsonify(students)

@app.route('/attendance', methods=['POST'])
@jwt_required()
def mark_attendance():
    data = request.json
    app.logger.debug(f"Mark attendance endpoint called with data: {data}")
    Attendance.mark_attendance(data['student_id'], data['subject'])
    return jsonify({"message": "Attendance marked"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
