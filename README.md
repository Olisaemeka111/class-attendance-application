# class-attendance-application

## Overview
A Flask + MongoDB attendance tracking system with teacher authentication and subject-based attendance.

## Setup & Installation
1. Clone the repository.
2. Navigate to the `attendance_system` directory.
3. Build and run the Docker containers:
    ```sh
    docker-compose up --build
    ```
4. Access the application at `http://localhost:5000`.

## Endpoints
- `GET /` - Home
- `POST /auth/register` - Register
- `POST /auth/login` - Login
- `GET /students` - Get all students
- `POST /attendance` - Mark attendance
