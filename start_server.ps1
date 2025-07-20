# OpenBanking MCP Server - PowerShell Startup Script
# Run this script in PowerShell to start the server

Write-Host "OpenBanking MCP Server - PowerShell Startup" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "requirements.txt")) {
    Write-Host "Error: requirements.txt not found. Please run this script from the project root directory." -ForegroundColor Red
    pause
    exit 1
}

# Activate conda environment
Write-Host "Activating conda environment: openbanking-backend" -ForegroundColor Yellow
conda activate openbanking-backend

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to activate conda environment 'openbanking-backend'" -ForegroundColor Red
    Write-Host "Please make sure the environment exists and conda is properly installed" -ForegroundColor Red
    pause
    exit 1
}

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install dependencies" -ForegroundColor Red
    pause
    exit 1
}

# Check if Ollama is running
Write-Host "Checking Ollama server..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✓ Ollama server is running" -ForegroundColor Green
} catch {
    Write-Host "⚠ Warning: Ollama server is not accessible at localhost:11434" -ForegroundColor Yellow
    Write-Host "Please make sure Ollama is installed and running" -ForegroundColor Yellow
    Write-Host "You can start Ollama by running 'ollama serve' in another terminal" -ForegroundColor Yellow
}

# Run the server
Write-Host "Starting MCP Server..." -ForegroundColor Yellow
python src/main.py

Write-Host "Server stopped. Press any key to exit..." -ForegroundColor Gray
pause
