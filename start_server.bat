@echo off
echo OpenBanking MCP Server - Windows Startup
echo =======================================

REM Activate conda environment
echo Activating conda environment: openbanking-backend
call conda activate openbanking-backend

REM Check if activation was successful
if %errorlevel% neq 0 (
    echo Error: Failed to activate conda environment 'openbanking-backend'
    echo Please make sure the environment exists and conda is properly installed
    pause
    exit /b 1
)

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

REM Run the server
echo Starting MCP Server...
python src/main.py

pause
