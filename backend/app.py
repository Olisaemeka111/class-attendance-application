# backend/app.py
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from database.connection import db
from database.student_model import Student
from database.attendance_model import Attendance
from database.user_model import User
import config

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET
jwt = JWTManager(app)

db.connect()

@app.route('/')
def home():
    return jsonify({"message": "Attendance System API Running"})

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    if User.create_user(data['username'], data['password']):
        return jsonify({"message": "User registered successfully"})
    return jsonify({"error": "User already exists"}), 400

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    user = User.authenticate(data['username'], data['password'])
    if user:
        token = create_access_token(identity=data['username'])
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    students = Student.get_all()
    return jsonify(students)

@app.route('/attendance', methods=['POST'])
@jwt_required()
def mark_attendance():
    data = request.json
    Attendance.mark_attendance(data['student_id'], data['subject'])
    return jsonify({"message": "Attendance marked"})

if __name__ == '__main__':
    app.run(debug=True)
