#!/bin/bash

# Quick installation script for Linux/Mac

echo "========================================"
echo " Multilingual Chatbot - Quick Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.10 or higher"
    exit 1
fi

echo "[1/5] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create virtual environment"
    exit 1
fi

echo "[2/5] Activating virtual environment..."
source venv/bin/activate

echo "[3/5] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi

echo ""
echo "========================================"
echo " Installation Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Create .env file with your credentials"
echo "2. Download gcp-credentials.json"
echo "3. Run: python setup.py"
echo "4. Run: python test_services.py"
echo "5. Run: streamlit run app.py"
echo ""
echo "See CHECKLIST.md for detailed instructions"
echo ""

