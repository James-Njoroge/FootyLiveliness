#!/bin/bash

echo "=================================="
echo "Setting up Backend API"
echo "=================================="

cd api

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "=================================="
echo "✓ Backend setup complete!"
echo "=================================="
echo ""
echo "To run the backend:"
echo "  cd api"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
