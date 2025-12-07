#!/bin/bash

echo "================================================================================"
echo "⚽ FOOTY LIVELINESS - STARTING WEB APP"
echo "================================================================================"
echo ""

# Check if model exists
if [ ! -f "model.pkl" ]; then
    echo "📊 Training model..."
    python3 train_and_save_model.py
    echo ""
fi

# Kill any existing servers on these ports
echo "🧹 Cleaning up old servers..."
lsof -ti:5001 | xargs kill -9 2>/dev/null
lsof -ti:8000 | xargs kill -9 2>/dev/null
sleep 1

# Start Flask API
echo "🔌 Starting API server on http://localhost:5001..."
python3 app.py > api.log 2>&1 &
API_PID=$!
echo "   API PID: $API_PID"

# Wait for API to start
sleep 3

# Start HTTP server for frontend
echo "🌐 Starting web server on http://localhost:8000..."
python3 -m http.server 8000 > web.log 2>&1 &
WEB_PID=$!
echo "   Web PID: $WEB_PID"

# Wait for web server to start
sleep 2

echo ""
echo "================================================================================"
echo "✅ WEB APP IS RUNNING!"
echo "================================================================================"
echo ""
echo "  🌐 Open in browser: http://localhost:8000"
echo "  🔌 API endpoint:    http://localhost:5001/api/upcoming"
echo ""
echo "  Logs:"
echo "    API:  tail -f api.log"
echo "    Web:  tail -f web.log"
echo ""
echo "  To stop: Press Ctrl+C or run: kill $API_PID $WEB_PID"
echo ""
echo "================================================================================"
echo ""

# Open in browser
open http://localhost:8000

# Save PIDs to file for easy cleanup
echo "$API_PID" > .api.pid
echo "$WEB_PID" > .web.pid

# Wait for user interrupt
trap "echo ''; echo 'Stopping servers...'; kill $API_PID $WEB_PID 2>/dev/null; rm -f .api.pid .web.pid api.log web.log; echo 'Stopped.'; exit 0" INT

# Keep script running
wait
