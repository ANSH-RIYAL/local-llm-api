#!/bin/bash

# Start the FastAPI server in the background
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 &

# Wait a moment for the server to start
sleep 2

# Start localtunnel
npx localtunnel --port 8001 --subdomain your-preferred-subdomain 