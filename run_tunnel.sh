#!/bin/bash

# Function to cleanup on exit
cleanup() {
    echo "Cleaning up..."
    kill $(jobs -p) 2>/dev/null || true
}

# Set up trap for cleanup
trap cleanup EXIT

# Check if localtunnel is installed
if ! command -v lt &> /dev/null; then
    echo "localtunnel is not installed. Installing..."
    if ! command -v npm &> /dev/null; then
        echo "Error: npm is not installed. Please install Node.js and npm first."
        exit 1
    fi
    npm install -g localtunnel
fi

# Check if server is running
if ! curl -s http://localhost:8050/ &> /dev/null; then
    echo "Error: FastAPI server is not running on port 8050"
    echo "Please start the server first using ./run_server.sh"
    exit 1
fi

echo "Starting localtunnel..."
lt --port 8050

# Keep the script running
wait 