#!/bin/bash

# Function to cleanup on exit
cleanup() {
    echo "Cleaning up..."
    deactivate 2>/dev/null || true
}

# Set up trap for cleanup
trap cleanup EXIT

# Function to check if port is in use
check_port() {
    if lsof -i:$1 >/dev/null 2>&1; then
        echo "Port $1 is already in use. Please stop any running server first."
        exit 1
    fi
}

# Check if ports are available
check_port 8050

echo "Activating virtual environment..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate

echo "Installing requirements..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "No requirements.txt found. Please ensure it exists."
    exit 1
fi

echo "Starting FastAPI server..."
python3 main.py 