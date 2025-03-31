#!/bin/bash

# Function to cleanup background processes
cleanup() {
    echo "Cleaning up..."
    kill $(jobs -p) 2>/dev/null
    exit
}

# Set up trap for cleanup on script exit
trap cleanup EXIT

# Start ngrok tunnel
echo "Starting ngrok tunnel..."
ngrok http 8050

# Keep the script running
wait 