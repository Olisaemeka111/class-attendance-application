#!/bin/bash

# Source the virtual environment
. venv/bin/activate

# Install the required packages
python -m pip install -r attendance_system/backend/requirements.txt
python -m pip install flask_jwt_extended pymongo

# Set PYTHONPATH
export PYTHONPATH=$(pwd)/attendance_system

# Start the backend server
cd "$(dirname "$0")/attendance_system/backend"

# Check if the port is already in use and kill the process using it
if lsof -i:5000; then
    echo "Port 5000 is already in use. Attempting to free the port..."
    fuser -k 5000/tcp
    sleep 2
fi

python app.py --host=0.0.0.0 &
BACKEND_PID=$!

# Wait for a few seconds to ensure the backend server has time to start
sleep 5

# Check if the backend server is running
if pgrep -f "python app.py" > /dev/null; then
    echo "Backend server is running."
else
    echo "Failed to start backend server."
    exit 1
fi

# Verify backend server status
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health)
if [ "$BACKEND_STATUS" -ne 200 ]; then
    echo "Backend server is not responding correctly. HTTP status code: $BACKEND_STATUS"
    kill $BACKEND_PID
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null
then
    echo "npm could not be found, installing Node.js and npm..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Run the front end application
cd ../frontend

# Check if package.json exists
if [ -f "package.json" ]; then
    # Check if script.js, styles.css, and index.js exist
    if [ ! -f "script.js" ]; then
        echo "Required file script.js not found in frontend directory, cannot start front end application."
        exit 1
    fi
    if [ ! -f "styles.css" ]; then
        echo "Required file styles.css not found in frontend directory, cannot start front end application."
        exit 1
    fi
    if [ ! -f "src/index.js" ]; then
        echo "Required file src/index.js not found in frontend directory, cannot start front end application."
        exit 1
    fi
    npm install
    # Automatically confirm the prompt for adding default browsers
    yes | npx browserslist --update-db
    npm start &
    FRONTEND_PID=$!
else
    echo "package.json not found, cannot start front end application."
    exit 1
fi

# Check if the front end application is running
if pgrep -f "npm start" > /dev/null; then
    echo "Front end application is running."
    echo "You can access the application at http://localhost:3000"
else
    echo "Failed to start front end application."
    kill $BACKEND_PID
    exit 1
fi

# Check if the script is running on Windows
if [[ "$OSTYPE" == "msys" ]]; then
    echo "On Windows, please set the execution policy to allow running this script:"
    echo "PowerShell command: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
fi

# Wait for both backend and frontend to finish
wait $BACKEND_PID
wait $FRONTEND_PID
