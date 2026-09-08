@echo off
title Alhrbi Tool - Installer
color 0A
cls

cd /d "%~dp0"

echo ==========================================
echo    Alhrbi Tool - Setup ^& Installer
echo ==========================================
echo.
echo [*] Checking Python installation...
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Python not found! Please install Python 3.8+
    echo.
    echo [*] Download Python: https://python.org/downloads
    echo.
    pause
    exit /b 1
)

echo [OK] Python found!
echo.

echo [*] Installing required packages...
echo.

pip uninstall --quiet -y discord.py discord discord.py-self
pip install --quiet discord.py-self
echo [OK] discord.py-self installed

pip install --quiet colorama
echo [OK] colorama installed

pip install --quiet aiohttp
echo [OK] aiohttp installed

echo.
echo ==========================================
echo    All packages installed successfully!
echo ==========================================
echo.
echo [*] To run the tool:
echo      - Double click "run.bat"
echo      - Or type: python alhrbi.py
echo.
pause
