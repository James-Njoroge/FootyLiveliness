#!/bin/bash

# Footy Liveliness - One-Command Setup Script
# Run this on a fresh computer to set up everything

set -e  # Exit on any error

echo "🚀 Setting up Footy Liveliness..."
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required but not installed. Install from https://python.org"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed. Install from https://nodejs.org"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "❌ npm is required but not installed."; exit 1; }

echo "✅ Python $(python3 --version) found"
echo "✅ Node $(node --version) found"
echo "✅ npm $(npm --version) found"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt
echo "✅ Python dependencies installed"
echo ""

# Install Node dependencies
echo "📦 Installing Node.js dependencies..."
npm install
echo "✅ Node.js dependencies installed"
echo ""

# Create data directory if needed
echo "📁 Setting up data directories..."
mkdir -p ../data/current_season
echo "✅ Directories created"
echo ""

# Start services
echo "🎉 Setup complete!"
echo ""
echo "════════════════════════════════════════════════════════════"
echo "                    READY TO START                          "
echo "════════════════════════════════════════════════════════════"
echo ""
echo "To start the application, run:"
echo ""
echo "  make start"
echo ""
echo "Or manually:"
echo ""
echo "  Terminal 1: python3 app.py"
echo "  Terminal 2: npm start"
echo ""
echo "The app will be available at:"
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:5001"
echo ""
echo "════════════════════════════════════════════════════════════"
