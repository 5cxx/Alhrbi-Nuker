@echo off
title Alhrbi Tool
color 0A
cls

cd /d "%~dp0"

echo ==========================================
echo           Alhrbi Tool
echo ==========================================
echo.
echo [*] Starting...
echo.

python alhrbi.py

if %errorlevel% neq 0 (
    echo.
    echo [X] Error occurred! Make sure:
    echo     1. File name is: alhrbi.py
    echo     2. All packages are installed
    echo     3. Run setup.bat first
    echo.
)

pause
