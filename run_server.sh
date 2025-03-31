#!/bin/bash

# Function to cleanup background processes
cleanup() {
    echo "Cleaning up..."
    kill $(jobs -p) 2>/dev/null
    exit
}

# Set up trap for cleanup on script exit
trap cleanup EXIT

# Start the FastAPI server
echo "Starting FastAPI server..."
python3 -m uvicorn main:app --host 0.0.0.0 --port 8001 &

# Wait a moment for the server to start
sleep 2

# Check if the server is running
if ! curl -s http://localhost:8001/ > /dev/null; then
    echo "Error: FastAPI server failed to start"
    exit 1
fi

echo "FastAPI server is running on http://localhost:8001"

# Keep the script running
wait 