@echo off
title Pune Estate — Intelligence Dashboard
color 0B
cls

echo.
echo  ============================================================
echo    PUNE ESTATE — AI Intelligence Dashboard
echo  ============================================================
echo.
echo  [1/3] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python not found!
    echo  Please install Python from https://python.org
    pause
    exit /b 1
)
echo  Python OK

echo.
echo  [2/3] Installing required packages...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo  WARNING: Some packages may not have installed correctly.
)
echo  Packages OK

echo.
echo  [3/3] Starting dashboard server...
echo.
echo  ============================================================
echo    Dashboard is running at: http://localhost:5000
echo    Opening in your browser...
echo.
echo    Press CTRL+C to stop the server
echo  ============================================================
echo.

:: Open browser after 3 seconds
start "" /b cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:5000"

:: Start server
python server.py

echo.
echo  Server stopped.
pause
