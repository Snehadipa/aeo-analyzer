#!/bin/bash

# Startup script for AI Product Visibility Analyzer on macOS/Linux

echo ""
echo "============================================================"
echo "     AI Product Visibility Analyzer"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python from https://www.python.org/downloads/"
    exit 1
fi

echo "[1/4] Checking Python version..."
python3 --version

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "[2/4] Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment"
        exit 1
    fi
    echo "       Virtual environment created"
else
    echo ""
    echo "[2/4] Using existing virtual environment..."
fi

# Activate virtual environment
echo ""
echo "[3/4] Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "[4/4] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi

# Check for .env file
echo ""
if [ ! -f ".env" ]; then
    echo "[WARNING] .env file not found"
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "[IMPORTANT] Edit .env and add your OpenAI API key!"
    echo "Visit: https://platform.openai.com/api-keys"
    echo ""
    read -p "Press Enter after you've added your API key..."
fi

# Start the server
echo ""
echo "============================================================"
echo "     Starting Server..."
echo "============================================================"
echo ""
echo "API running at: http://localhost:8000"
echo "Documentation at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 main.py
