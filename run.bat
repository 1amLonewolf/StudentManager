@echo off
title Student Manager
color 0A
cls

echo ========================================
echo   Student Manager - Starting...
echo ========================================
echo.

cd /d "%~dp0"

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    venv\Scripts\pip install -r requirements.txt --quiet
)

if not exist "instance" mkdir instance

echo.
echo ========================================
echo   Student Manager is running!
echo   Open: http://localhost:5000
echo   Login: admin / admin123
echo ========================================
echo.
echo Press Ctrl+C to stop
echo.

python app.py

pause
