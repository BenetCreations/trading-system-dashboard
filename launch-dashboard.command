#!/bin/bash
# ─────────────────────────────────────────────────────
# Trading Dashboard Launcher
# Double-click this file to start the dashboard.
# It launches a local web server and opens Chrome.
# Press Ctrl+C in the terminal window to stop.
# ─────────────────────────────────────────────────────

# Move to the folder this script lives in (where the HTML file is)
cd "$(dirname "$0")"

PORT=8080

# Check if port is already in use
if lsof -i :$PORT -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Port $PORT already in use — opening dashboard in browser."
  open -a "Google Chrome" "http://localhost:$PORT/trading-dashboard.html"
  exit 0
fi

echo "Starting local server on port $PORT…"
echo "Dashboard: http://localhost:$PORT/trading-dashboard.html"
echo ""
echo "Press Ctrl+C to stop the server."
echo ""

# Start the server in the background
python3 server.py $PORT &
SERVER_PID=$!

# Wait until the server is actually responding before opening the browser
for i in {1..20}; do
  if curl -s -o /dev/null "http://localhost:$PORT/" 2>/dev/null; then
    break
  fi
  sleep 0.25
done

# Open in Chrome specifically
open -a "Google Chrome" "http://localhost:$PORT/trading-dashboard.html"

# Bring the server back to the foreground so Ctrl+C stops it
wait $SERVER_PID
