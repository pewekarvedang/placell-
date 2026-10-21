@echo off
title Placell - Unified Server
cd /d "%~dp0"

echo =====================================================================
echo  Placell: AI-Powered Student Placement Experience and Career Analytics
echo  Solo Developer: Vedang Pewekar (B.Tech CSBS)
echo =====================================================================
echo.

echo [1/3] Checking compiled frontend static assets...
if not exist "frontend\dist\index.html" (
    echo Compiling frontend bundle via Vite...
    call npm --prefix frontend run build
) else (
    echo Frontend build found in frontend\dist\
)

echo.
echo [2/3] Checking port 8000 availability...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    echo Freeing port 8000 held by previous process %%a...
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo [3/3] Starting Placell Unified Server on http://127.0.0.1:8000 ...
echo - Web Application: http://127.0.0.1:8000
echo - Swagger API Docs: http://127.0.0.1:8000/docs
echo.
echo Press Ctrl+C in this terminal to stop the server.
echo.

set PYTHONPATH=backend

start "" "http://127.0.0.1:8000"

py -m uvicorn app.main:app --host 127.0.0.1 --port 8000
if %errorlevel% neq 0 (
    "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000
)

pause
