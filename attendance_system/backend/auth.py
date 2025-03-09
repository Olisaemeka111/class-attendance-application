from flask import Blueprint, request, jsonify

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    # ...existing code...
    return jsonify({"message": "Login successful"})

@auth.route('/register', methods=['POST'])
def register():
    # ...existing code...
    return jsonify({"message": "Registration successful"})