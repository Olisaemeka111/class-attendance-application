import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb+srv://<username>:<password>@cluster0.mongodb.net/attendance_db?retryWrites=true&w=majority'
    JWT_SECRET = "your_jwt_secret_key"
    MONGO_DB_NAME = "attendance_db"
    SERVER_NAME = os.environ.get('SERVER_NAME') or 'localhost:5000'
