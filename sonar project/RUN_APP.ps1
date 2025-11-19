# SONAR Rock vs Mine Prediction - Flask App Runner (PowerShell)
# This script runs the Flask app with the correct Python environment

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   SONAR ROCK vs MINE PREDICTION - FLASK APPLICATION" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Change to script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Use conda Python (3.11) which has all dependencies installed
Write-Host "Starting Flask application with Python 3.11..." -ForegroundColor Green
Write-Host ""

# Run the Flask app
& C:\Users\noman\anaconda3\python.exe app_sonar_predict.py

Write-Host ""
Write-Host "Application stopped." -ForegroundColor Yellow
