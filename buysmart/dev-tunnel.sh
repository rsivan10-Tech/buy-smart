#!/usr/bin/env bash
set -euo pipefail

# One script to run backend + frontend + ngrok tunnels for live share.
# Usage: bash dev-tunnel.sh
# Requires: python3, npm, uvicorn, ngrok, lsof/grep

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$BASE_DIR/backend"
FRONTEND_DIR="$BASE_DIR/frontend"

# ensure env for frontend backend URL
cat > "$FRONTEND_DIR/.env.local" <<EOF
NEXT_PUBLIC_BACKEND_URL=http://127.0.0.1:8005
EOF

# kill previous instances gracefully if exist
kill_port() {
  local port=$1
  if lsof -i :$port -t >/dev/null 2>&1; then
    echo "Killing process on port $port"
    lsof -i :$port -t | xargs -r kill -9
  fi
}
kill_port 8005
kill_port 3006

# start backend
echo "Starting backend on 8005..."
cd "$BACKEND_DIR"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8005 &
BACKEND_PID=$!
sleep 2

# start frontend
echo "Starting frontend on 3006..."
cd "$FRONTEND_DIR"
npm run dev -- --port 3006 &
FRONTEND_PID=$!
sleep 2

# start tunnels
echo "Starting ngrok for frontend and backend..."
ngrok http 3006 > /tmp/ngrok_frontend.log 2>&1 &
NGROK_FE_PID=$!
ngrok http 8005 > /tmp/ngrok_backend.log 2>&1 &
NGROK_BE_PID=$!

sleep 4

print_url() {
  local log=$1
  if grep -q "HTTP" "$log"; then
    grep "forwarding" "$log" | awk '{print $2" " $3}' | head -n 2
  else
    echo "ngrok startup possibly still in progress";
  fi
}

echo "\n--- status ---"
ps -p $BACKEND_PID >/dev/null && echo "backend running ($BACKEND_PID)" || echo "backend stopped"
ps -p $FRONTEND_PID >/dev/null && echo "frontend running ($FRONTEND_PID)" || echo "frontend stopped"
ps -p $NGROK_FE_PID >/dev/null && echo "ngrok frontend running ($NGROK_FE_PID)" || echo "ngrok frontend stopped"
ps -p $NGROK_BE_PID >/dev/null && echo "ngrok backend running ($NGROK_BE_PID)" || echo "ngrok backend stopped"

echo "\nFrontend ngrok URL(s):"
print_url /tmp/ngrok_frontend.log

echo "\nBackend ngrok URL(s):"
print_url /tmp/ngrok_backend.log

echo "\nTo stop, run: kill $BACKEND_PID $FRONTEND_PID $NGROK_FE_PID $NGROK_BE_PID"
