@echo off
REM SONAR Rock vs Mine Prediction - Flask App Runner
REM This script runs the Flask app with the correct Python environment

echo.
echo ============================================================
echo    SONAR ROCK vs MINE PREDICTION - FLASK APPLICATION
echo ============================================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Use conda Python (3.11) which has all dependencies installed
echo Starting Flask application...
echo.

C:\Users\noman\anaconda3\python.exe app_sonar_predict.py

pause
