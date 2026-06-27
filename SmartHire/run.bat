@echo off
title SmartHire - AI Career Platform
color 0A

echo.
echo  ================================================
echo   SmartHire - AI Career Guidance Platform
echo  ================================================
echo.

REM ── Check Python ──────────────────────────────────
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo  [ERROR] Python is NOT installed or not in PATH.
    echo.
    echo  Please install Python 3.11 from:
    echo  https://www.python.org/downloads/
    echo.
    echo  IMPORTANT: Check "Add Python to PATH" during install!
    echo.
    pause
    start https://www.python.org/downloads/
    exit /b 1
)

echo  [OK] Python found:
python --version
echo.

REM ── Install / upgrade pip ─────────────────────────
echo  [INFO] Upgrading pip...
python -m pip install --upgrade pip --quiet

REM ── Install requirements ──────────────────────────
echo  [INFO] Installing requirements (first run may take 1-2 minutes)...
echo.
python -m pip install -r requirements.txt --quiet

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo  [ERROR] Failed to install some packages.
    echo  Try running as Administrator or check your internet connection.
    pause
    exit /b 1
)

echo.
echo  [OK] All packages installed.
echo.
echo  ================================================
echo   Starting SmartHire on http://localhost:8501
echo   Press Ctrl+C to stop the app
echo  ================================================
echo.

REM ── Launch Streamlit ──────────────────────────────
python -m streamlit run streamlit_app.py --server.port 8501 --server.address localhost --browser.serverAddress localhost

pause
