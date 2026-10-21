@echo off
title Placell - Development Environment (Vite + FastAPI HMR)
echo =====================================================================
echo  Placell: Development Launcher (Concurrent Backend & Frontend)
echo =====================================================================
echo.

cd /d "%~dp0"

echo Starting Backend API Server (Port 8000)...
start "Placell - Backend API (Uvicorn)" cmd /k "cd backend && set PYTHONPATH=. && py -m uvicorn app.main:app --reload --port 8000"

echo Starting Frontend Dev Server (Port 5173)...
start "Placell - Frontend Client (Vite)" cmd /k "cd frontend && npm run dev"

echo.
echo Development services launched:
echo - Frontend: http://localhost:5173
echo - Backend:  http://localhost:8000
echo - Swagger:  http://localhost:8000/docs
echo.
