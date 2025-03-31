@echo off
echo Starting ShelfTrack Frontend...
echo.

REM Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.x
    pause
    exit /b 1
)

REM Set Python encoding to UTF-8
set PYTHONIOENCODING=utf-8

REM Check if required packages are installed
echo Checking and installing required packages...
python -m pip install -r frontend/requirements.txt

REM Change to the frontend directory and run the application
cd frontend
echo Starting the frontend server...
echo.
python -X utf8 main.py

if errorlevel 1 (
    echo.
    echo Error running the frontend server!
    pause
) else (
    echo.
    echo Frontend server stopped.
    pause
)