@echo off
title Spam Email Detector - Streamlit Launcher

REM Change directory to this script location
cd /d "%~dp0"

REM Start Streamlit on a fixed port
start "" cmd /c python -m streamlit run app.py --server.port 8501 --server.headless true

REM Wait a moment for server to start
timeout /t 2 >nul

REM Open in default browser
start "" http://localhost:8501

echo.
echo Streamlit app is running at: http://localhost:8501
echo Close this window to stop the launcher (app keeps running in another window).
pause
