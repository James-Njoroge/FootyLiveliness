# Footy Liveliness - Makefile
# Automates setup and running of the application

.PHONY: help install install-python install-node scrape scrape-upcoming update start-api start-frontend start stop status clean test check-ports kill-ports

# Default target - show help
help:
	@echo "╔════════════════════════════════════════════════════════════════╗"
	@echo "║         Footy Liveliness - Automated Setup & Run              ║"
	@echo "╚════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Available commands:"
	@echo ""
	@echo "  make install          - Install all dependencies (Python + Node)"
	@echo "  make scrape           - Scrape all season fixtures from FotMob"
	@echo "  make scrape-upcoming  - Scrape only upcoming fixtures (faster)"
	@echo "  make update           - Re-scrape data and restart application"
	@echo "  make start            - Start both API and frontend"
	@echo "  make start-api        - Start Flask API only"
	@echo "  make start-frontend   - Start React frontend only"
	@echo "  make stop             - Stop all running processes"
	@echo "  make status           - Check application status"
	@echo "  make clean            - Clean up temporary files"
	@echo "  make kill-ports       - Kill processes on ports 5001 and 3000"
	@echo "  make test             - Test API endpoints"
	@echo "  make check-ports      - Check if ports are available"
	@echo ""
	@echo "Quick Start:"
	@echo "  1. make install       (one-time setup)"
	@echo "  2. make start         (starts everything)"
	@echo ""
	@echo "Or run everything in one command:"
	@echo "  make install && make start"
	@echo ""

# Install all dependencies
install: install-python install-node
	@echo "✅ All dependencies installed!"
	@echo ""
	@echo "Next step: Run 'make start' to launch the application"

# Install Python dependencies
install-python:
	@echo "📦 Installing Python dependencies..."
	pip3 install flask flask-cors pandas numpy scikit-learn requests
	@echo "✅ Python dependencies installed"

# Install Node dependencies
install-node:
	@echo "📦 Installing Node.js dependencies..."
	npm install
	@echo "✅ Node.js dependencies installed"

# Scrape all season fixtures from FotMob (past + future)
scrape:
	@echo "🌐 Scraping all season fixtures from FotMob (this may take a few minutes)..."
	python3 scrape_all_season_fixtures.py
	@echo "✅ All fixtures scraped and saved"

# Scrape only upcoming fixtures (faster)
scrape-upcoming:
	@echo "🌐 Scraping upcoming fixtures from FotMob..."
	python3 scrape_upcoming_fixtures.py
	@echo "✅ Upcoming fixtures scraped and saved"

# Update: Re-scrape data and restart application
update:
	@echo "╔════════════════════════════════════════════════════════════════╗"
	@echo "║              Updating Footy Liveliness Data                    ║"
	@echo "╚════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📊 Step 1/3: Stopping application..."
	@$(MAKE) stop
	@echo ""
	@echo "🌐 Step 2/3: Re-scraping fixtures from FotMob..."
	@$(MAKE) scrape
	@echo ""
	@echo "🚀 Step 3/3: Restarting application with new data..."
	@$(MAKE) start
	@echo ""
	@echo "╔════════════════════════════════════════════════════════════════╗"
	@echo "║              ✅ Update Complete!                               ║"
	@echo "╚════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📱 Application running with latest data at http://localhost:3000"
	@echo "🔄 New predictions loaded from updated fixtures"

# Check if ports are available
check-ports:
	@echo "🔍 Checking if ports 5001 and 3000 are available..."
	@if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null 2>&1; then \
		echo "⚠️  Port 5001 is in use. Run 'make kill-ports' to free it."; \
	else \
		echo "✅ Port 5001 is available"; \
	fi
	@if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then \
		echo "⚠️  Port 3000 is in use. Run 'make kill-ports' to free it."; \
	else \
		echo "✅ Port 3000 is available"; \
	fi

# Kill processes on ports 5001 and 3000
kill-ports:
	@echo "🔪 Killing processes on ports 5001 and 3000..."
	@-lsof -ti:5001 | xargs kill -9 2>/dev/null || echo "Port 5001 already free"
	@-lsof -ti:3000 | xargs kill -9 2>/dev/null || echo "Port 3000 already free"
	@echo "✅ Ports freed"

# Start Flask API in background
start-api:
	@echo "🚀 Starting Flask API on http://localhost:5001..."
	@python3 app.py &
	@sleep 3
	@echo "✅ Flask API started"
	@echo "   Check: http://localhost:5001/api/health"

# Start React frontend in background
start-frontend:
	@echo "🚀 Starting React frontend on http://localhost:3000..."
	@npm start &
	@sleep 5
	@echo "✅ React frontend started"
	@echo "   Opening: http://localhost:3000"

# Start both API and frontend
start: kill-ports
	@echo "╔════════════════════════════════════════════════════════════════╗"
	@echo "║              Starting Footy Liveliness Application            ║"
	@echo "╚════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "🚀 Starting Flask API..."
	@python3 app.py > api.log 2>&1 & echo $$! > api.pid
	@sleep 3
	@if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null 2>&1; then \
		echo "✅ Flask API started on http://localhost:5001"; \
	else \
		echo "❌ Flask API failed to start. Check api.log for errors."; \
		exit 1; \
	fi
	@echo ""
	@echo "🚀 Starting React frontend..."
	@BROWSER=none npm start > frontend.log 2>&1 & echo $$! > frontend.pid
	@sleep 8
	@if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then \
		echo "✅ React frontend started on http://localhost:3000"; \
	else \
		echo "❌ React frontend failed to start. Check frontend.log for errors."; \
		exit 1; \
	fi
	@echo ""
	@echo "╔════════════════════════════════════════════════════════════════╗"
	@echo "║                    🎉 Application Ready!                       ║"
	@echo "╚════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📱 Open your browser to: http://localhost:3000"
	@echo ""
	@echo "API Endpoints:"
	@echo "  • Health:    http://localhost:5001/api/health"
	@echo "  • Upcoming:  http://localhost:5001/api/upcoming"
	@echo "  • Stats:     http://localhost:5001/api/stats"
	@echo ""
	@echo "Logs:"
	@echo "  • API:       tail -f api.log"
	@echo "  • Frontend:  tail -f frontend.log"
	@echo ""
	@echo "To stop: make stop"
	@echo ""

# Stop all running processes
stop:
	@echo "🛑 Stopping all processes..."
	@if [ -f api.pid ]; then \
		kill $$(cat api.pid) 2>/dev/null || true; \
		rm api.pid; \
		echo "✅ Flask API stopped"; \
	fi
	@if [ -f frontend.pid ]; then \
		kill $$(cat frontend.pid) 2>/dev/null || true; \
		rm frontend.pid; \
		echo "✅ React frontend stopped"; \
	fi
	@make kill-ports
	@echo "✅ All processes stopped"

# Test API endpoints
test:
	@echo "🧪 Testing API endpoints..."
	@echo ""
	@echo "1. Health check:"
	@curl -s http://localhost:5001/api/health | python3 -m json.tool || echo "❌ API not responding"
	@echo ""
	@echo "2. Stats endpoint:"
	@curl -s http://localhost:5001/api/stats | python3 -m json.tool || echo "❌ Stats endpoint failed"
	@echo ""
	@echo "3. Upcoming matches (first 2):"
	@curl -s http://localhost:5001/api/upcoming | python3 -c "import sys, json; data = json.load(sys.stdin); print(json.dumps(data[:2], indent=2))" || echo "❌ Upcoming endpoint failed"
	@echo ""
	@echo "✅ API tests complete"

# Clean up temporary files
clean:
	@echo "🧹 Cleaning up temporary files..."
	@rm -f api.log frontend.log api.pid frontend.pid
	@rm -rf __pycache__ .pytest_cache
	@find . -name "*.pyc" -delete
	@find . -name ".DS_Store" -delete
	@echo "✅ Cleanup complete"

# Full reset - clean and reinstall
reset: clean
	@echo "🔄 Performing full reset..."
	@rm -rf node_modules package-lock.json
	@echo "✅ Reset complete. Run 'make install' to reinstall dependencies."

# Development mode - start with auto-reload
dev: kill-ports
	@echo "🔧 Starting in development mode..."
	@echo ""
	@echo "Terminal 1: Flask API (with auto-reload)"
	@python3 app.py &
	@sleep 3
	@echo ""
	@echo "Terminal 2: React (with hot-reload)"
	@npm start

# Quick demo - install, scrape, and start
demo: install scrape start
	@echo ""
	@echo "╔════════════════════════════════════════════════════════════════╗"
	@echo "║                  🎬 Demo Mode Ready!                           ║"
	@echo "╚════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "The application is now running with live data!"
	@echo "Open http://localhost:3000 in your browser."
	@echo ""

# Show status of running processes
status:
	@echo "📊 Application Status:"
	@echo ""
	@if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null 2>&1; then \
		echo "✅ Flask API:      Running on port 5001"; \
	else \
		echo "❌ Flask API:      Not running"; \
	fi
	@if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then \
		echo "✅ React Frontend: Running on port 3000"; \
	else \
		echo "❌ React Frontend: Not running"; \
	fi
	@echo ""
	@if [ -f ../data/current_season/upcoming_fixtures.json ]; then \
		FIXTURE_COUNT=$$(python3 -c "import json; print(len(json.load(open('../data/current_season/upcoming_fixtures.json'))))"); \
		echo "📅 Fixtures loaded: $$FIXTURE_COUNT matches"; \
	else \
		echo "⚠️  No fixtures file found. Run 'make scrape' to fetch data."; \
	fi
	@echo ""

# Open application in browser
open:
	@echo "🌐 Opening application in browser..."
	@open http://localhost:3000 || xdg-open http://localhost:3000 || echo "Please open http://localhost:3000 manually"

# Show logs
logs:
	@echo "📜 Application Logs:"
	@echo ""
	@echo "=== Flask API Log ==="
	@tail -20 api.log 2>/dev/null || echo "No API logs found"
	@echo ""
	@echo "=== React Frontend Log ==="
	@tail -20 frontend.log 2>/dev/null || echo "No frontend logs found"

# Watch logs in real-time
watch-logs:
	@echo "👀 Watching logs (Ctrl+C to stop)..."
	@tail -f api.log frontend.log

# Validate installation
validate:
	@echo "✅ Validating installation..."
	@echo ""
	@echo "Python version:"
	@python3 --version
	@echo ""
	@echo "Node version:"
	@node --version
	@echo ""
	@echo "npm version:"
	@npm --version
	@echo ""
	@echo "Required Python packages:"
	@python3 -c "import flask; print('  ✅ flask:', flask.__version__)"
	@python3 -c "import pandas; print('  ✅ pandas:', pandas.__version__)"
	@python3 -c "import numpy; print('  ✅ numpy:', numpy.__version__)"
	@python3 -c "import sklearn; print('  ✅ scikit-learn:', sklearn.__version__)"
	@echo ""
	@echo "Model files:"
	@if [ -f model.pkl ]; then echo "  ✅ model.pkl"; else echo "  ❌ model.pkl missing"; fi
	@if [ -f scaler.pkl ]; then echo "  ✅ scaler.pkl"; else echo "  ❌ scaler.pkl missing"; fi
	@if [ -f team_stats.pkl ]; then echo "  ✅ team_stats.pkl"; else echo "  ❌ team_stats.pkl missing"; fi
	@echo ""
	@echo "✅ Validation complete"
