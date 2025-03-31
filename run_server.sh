#!/bin/bash

# Function to cleanup background processes
cleanup() {
    echo "Cleaning up..."
    kill $(jobs -p) 2>/dev/null
    exit
}

# Set up trap for cleanup on script exit
trap cleanup EXIT INT TERM

# Create and activate virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Set the model to TinyLlama
export MODEL_NAME="TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# Check if port 8050 is already in use
if lsof -i:8050 > /dev/null; then
    echo "Port 8050 is already in use. Please stop any running server first."
    exit 1
fi

# Start the FastAPI server
echo "Starting FastAPI server..."
python3 -m uvicorn main:app --host 0.0.0.0 --port 8050 &
server_pid=$!

# Wait for server to start (up to 30 seconds)
for i in {1..30}; do
    if curl -s http://localhost:8050/ > /dev/null; then
        echo "FastAPI server is running on http://localhost:8050"
        # Keep the script running
        wait $server_pid
        exit 0
    fi
    sleep 1
done

echo "Error: FastAPI server failed to start within 30 seconds"
exit 1 