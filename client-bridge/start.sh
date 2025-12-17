#!/bin/bash
set -e

# Validate environment variables
if [ -z "$DB_URL" ]; then
    echo "Error: DB_URL is not set"
    exit 1
fi

if [ -z "$AAAS_TOKEN" ]; then
    echo "Error: SAAS_TOKEN is not set"
    exit 1
fi

if [ -z "$AAAS_TUNNEL_HOST" ]; then
    echo "Error: SAAS_TUNNEL_HOST is not set. Example: http://saas.com:8080"
    exit 1
fi

if [ -z "$REMOTE_PORT" ]; then
    echo "Error: REMOTE_PORT is not set. Example: 10001"
    exit 1
fi

# local API port
API_PORT=8000

echo "Starting FastAPI Bridge..."
# Start FastAPI in background
uvicorn main:app --host 0.0.0.0 --port $API_PORT &
API_PID=$!

# Wait for API to be ready
echo "Waiting for API to be ready..."
sleep 2

echo "Starting Chisel Tunnel..."
echo "Connecting to $AAAS_TUNNEL_HOST..."
# Chisel Client: 
chisel client --auth "$AAAS_TOKEN" "$AAAS_TUNNEL_HOST" "R:$REMOTE_PORT:localhost:$API_PORT" &
CHISEL_PID=$!

# Handle shutdown
trap "kill $API_PID $CHISEL_PID; exit" SIGINT SIGTERM

# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?
