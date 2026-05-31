@echo off
REM Setup script for AI Chatbot (Windows)

echo ========================================
echo AI Chatbot - Setup Script
echo ========================================
echo.

REM Setup Backend
echo.
echo [1/4] Setting up Backend...
cd backend

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Copy .env.example to .env
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo Please edit backend\.env and add your API keys
)

cd ..

REM Setup Frontend
echo.
echo [2/4] Setting up Frontend...
cd frontend

REM Check if Node is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed or not in PATH
    pause
    exit /b 1
)

REM Install dependencies
echo Installing Node dependencies...
call npm install

cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Configure your API keys in backend\.env
echo 2. Start the backend:  cd backend ^& venv\Scripts\activate ^& uvicorn main:app --reload
echo 3. Start the frontend: cd frontend ^& npm start
echo.
echo Backend will run on http://localhost:8000
echo Frontend will run on http://localhost:3000
echo.
pause
