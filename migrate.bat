@echo off
REM Database Migration Helper Script

echo ========================================
echo   Student Manager - Database Migration
echo ========================================
echo.

cd /d "%~dp0"

REM Check if venv exists
if not exist "venv" (
    echo Error: Virtual environment not found!
    echo Please run run.bat first to set up the environment.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo.
echo Choose an option:
echo   1. Initialize migrations (first time only)
echo   2. Create a new migration
echo   3. Run migrations (upgrade database)
echo   4. Downgrade (undo last migration)
echo   5. Show migration history
echo   6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto init
if "%choice%"=="2" goto create
if "%choice%"=="3" goto upgrade
if "%choice%"=="4" goto downgrade
if "%choice%"=="5" goto history
if "%choice%"=="6" goto end

echo Invalid choice!
pause
exit /b 1

:init
echo.
echo Initializing migrations...
flask db init
echo.
echo Migration folder created!
echo Next steps:
echo   1. Run option 2 to create initial migration
echo   2. Run option 3 to apply migrations
pause
goto end

:create
echo.
set /p message="Enter migration message: "
flask db migrate -m "%message%"
echo.
echo Migration created! Review the files in migrations/ folder.
echo Then run option 3 to apply the migration.
pause
goto end

:upgrade
echo.
echo Applying migrations...
flask db upgrade
echo.
echo Database upgraded successfully!
pause
goto end

:downgrade
echo.
echo Rolling back last migration...
flask db downgrade -1
echo.
echo Database rolled back!
pause
goto end

:history
echo.
echo Migration history:
flask db history
pause
goto end

:end
