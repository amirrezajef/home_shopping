#!/bin/bash

echo "Starting Home Shopping Application..."
echo

echo "Starting Flask API Server..."
cd api
python app.py &
API_PID=$!
cd ..

echo "Waiting for API server to start..."
sleep 5

echo "Starting React Frontend..."
cd frontend
npm start &
REACT_PID=$!
cd ..

echo
echo "Application is starting..."
echo "Flask API: http://localhost:5000"
echo "React App: http://localhost:3000"
echo
echo "Press Ctrl+C to stop all services..."

# Function to cleanup background processes
cleanup() {
    echo
    echo "Stopping services..."
    kill $API_PID 2>/dev/null
    kill $REACT_PID 2>/dev/null
    exit 0
}

# Set trap to cleanup on exit
trap cleanup SIGINT SIGTERM

# Wait for user to press Ctrl+C
wait 