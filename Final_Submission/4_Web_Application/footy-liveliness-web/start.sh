#!/bin/bash

echo "================================================================================"
echo "⚽ FOOTY LIVELINESS WEB APP"
echo "================================================================================"
echo ""
echo "Starting the web application..."
echo ""

# Check if model exists
if [ ! -f "model.pkl" ]; then
    echo "Model not found. Training model..."
    python3 train_and_save_model.py
    echo ""
fi

# Start Flask API in background
echo "Starting API server on http://localhost:5000..."
python3 app.py &
API_PID=$!

# Wait for API to start
sleep 3

# Open web app in browser
echo "Opening web app in browser..."
open index.html

echo ""
echo "================================================================================"
echo "✓ WEB APP RUNNING!"
echo "================================================================================"
echo ""
echo "  🌐 Web App: Open index.html in your browser"
echo "  🔌 API: http://localhost:5000"
echo ""
echo "  Endpoints:"
echo "    GET  /api/upcoming  - Ranked fixtures"
echo "    GET  /api/stats     - Model statistics"
echo "    POST /api/predict   - Predict single match"
echo ""
echo "  Press Ctrl+C to stop the server"
echo ""
echo "================================================================================"

# Wait for user to stop
wait $API_PID
