@echo off
title Blood Donor Intelligence System

cd /d "%~dp0"

echo.
echo ============================================
echo    BLOOD DONOR INTELLIGENCE SYSTEM
echo ============================================
echo.

if not exist "venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found.
    echo.
    echo Please run setup_windows.ps1 first.
    echo.
    pause
    exit /b 1
)

echo [1/3] Starting FastAPI backend...
echo.

start "FastAPI Backend" /D "%~dp0" "%~dp0venv\Scripts\python.exe" -m uvicorn app.main:app --reload

echo FastAPI starting...
timeout /t 5 /nobreak > nul

echo.
echo [2/3] Starting Streamlit dashboard...
echo.

start "Streamlit Dashboard" /D "%~dp0" "%~dp0venv\Scripts\python.exe" -m streamlit run dashboard\app.py

echo.
echo [3/3] Opening dashboard...
echo.

timeout /t 5 /nobreak > nul

start "" "http://localhost:8501"

echo.
echo ============================================
echo    APPLICATION STARTED
echo ============================================
echo.
echo FastAPI:
echo http://127.0.0.1:8000
echo.
echo Swagger:
echo http://127.0.0.1:8000/docs
echo.
echo Dashboard:
echo http://localhost:8501
echo.
echo ============================================
echo.

pause