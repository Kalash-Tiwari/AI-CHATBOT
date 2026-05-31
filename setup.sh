#!/bin/bash
# Setup script for AI Chatbot (macOS/Linux)

echo "========================================"
echo "AI Chatbot - Setup Script"
echo "========================================"
echo ""

# Setup Backend
echo ""
echo "[1/2] Setting up Backend..."
cd backend

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Copy .env.example to .env
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit backend/.env and add your API keys"
fi

cd ..

# Setup Frontend
echo ""
echo "[2/2] Setting up Frontend..."
cd frontend

# Check if Node is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed"
    exit 1
fi

# Install dependencies
echo "Installing Node dependencies..."
npm install

cd ..

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Configure your API keys in backend/.env"
echo "2. Start the backend:  cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "3. Start the frontend: cd frontend && npm start"
echo ""
echo "Backend will run on http://localhost:8000"
echo "Frontend will run on http://localhost:3000"
echo ""
