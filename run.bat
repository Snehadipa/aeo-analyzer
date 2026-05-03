@echo off
REM Startup script for AI Product Visibility Analyzer on Windows

echo.
echo ============================================================
echo     AI Product Visibility Analyzer
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Checking Python version...
python --version

REM Check if virtual environment exists
if not exist "venv" (
    echo.
    echo [2/4] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo        Virtual environment created
) else (
    echo.
    echo [2/4] Using existing virtual environment...
)

REM Activate virtual environment
echo.
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo [4/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

REM Check for .env file
echo.
if not exist ".env" (
    echo [WARNING] .env file not found
    echo Please copy .env.example to .env and add your OpenAI API key
    echo.
    copy .env.example .env >nul
    echo .env file created from template
    echo.
    echo [IMPORTANT] Edit .env and add your OpenAI API key!
    echo Visit: https://platform.openai.com/api-keys
    pause
)

REM Start the server
echo.
echo ============================================================
echo     Starting Server...
echo ============================================================
echo.
echo API running at: http://localhost:8000
echo Documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py

pause
