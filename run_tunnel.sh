#!/bin/bash

# Function to cleanup background processes
cleanup() {
    echo "Cleaning up..."
    kill $(jobs -p) 2>/dev/null
    exit
}

# Set up trap for cleanup on script exit
trap cleanup EXIT

# Install localtunnel if not already installed
if ! command -v lt &> /dev/null; then
    echo "Installing localtunnel..."
    npm install -g localtunnel
fi

# Start localtunnel
echo "Starting localtunnel..."
lt --port 8050

# Keep the script running
wait 