@echo off
title Student Manager
cls
cd /d "%~dp0"

REM Quick start - assumes venv and dependencies exist
if exist "venv\Scripts\python.exe" (
    venv\Scripts\python app.py
) else (
    python app.py
)

pause
