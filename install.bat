@echo off
echo ============================================================
echo DIAGNOSTIC PRO SUITE ULTIMATE EDITION INSTALLER
echo Version: 2.0.0
echo ============================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Starting Python installer...
python install.py

if errorlevel 1 (
    echo Installation failed!
    pause
    exit /b 1
)

echo.
echo Installation completed successfully!
echo.
pause
