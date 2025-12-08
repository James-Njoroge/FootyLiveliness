#!/bin/bash

echo "============================================================"
echo "🚀 STARTING FOOTY LIVELINESS WITH LIVE DATA"
echo "============================================================"

# Step 1: Fetch upcoming matches
echo ""
echo "📡 Step 1: Fetching upcoming Premier League matches..."
echo "------------------------------------------------------------"
cd ../data
python3 scrape_upcoming_simple.py

if [ $? -ne 0 ]; then
    echo "⚠️  Warning: Could not fetch live data, using sample data"
else
    echo "✅ Live data fetched successfully"
fi

# Step 2: Start backend API
echo ""
echo "🔧 Step 2: Starting Backend API..."
echo "------------------------------------------------------------"
cd ../web-app/api
source venv/bin/activate
python app.py &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"

# Wait for backend to start
sleep 3

# Step 3: Start frontend
echo ""
echo "🎨 Step 3: Starting Frontend..."
echo "------------------------------------------------------------"
cd ..
npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID)"

echo ""
echo "============================================================"
echo "✅ ALL SYSTEMS RUNNING!"
echo "============================================================"
echo ""
echo "📊 Backend API:  http://localhost:5001"
echo "🌐 Frontend:     http://localhost:3000"
echo ""
echo "Press CTRL+C to stop all services"
echo "============================================================"

# Wait for user interrupt
trap "echo ''; echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
