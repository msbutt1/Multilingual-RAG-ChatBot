@echo off
REM Quick installation script for Windows

echo ========================================
echo  Multilingual Chatbot - Quick Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.11 or 3.12
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Create .env file with your credentials
echo 2. Download gcp-credentials.json
echo 3. Run: python setup.py
echo 4. Run: python test_services.py
echo 5. Run: streamlit run app.py
echo.
echo See CHECKLIST.md for detailed instructions
echo.
pause

