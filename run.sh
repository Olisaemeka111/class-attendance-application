#!/bin/bash

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r attendance_system/backend/requirements.txt

# Run the Flask application
export FLASK_APP=attendance_system/backend/app.py
export FLASK_ENV=development
flask run

# Check if the script is running on Windows
if [[ "$OSTYPE" == "msys" ]]; then
    echo "On Windows, please set the execution policy to allow running this script:"
    echo "PowerShell command: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
fi

# Command to run the script
./run.sh
