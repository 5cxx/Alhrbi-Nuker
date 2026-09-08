@echo off
title Alhrbi Tool - Installer
color 0A
cls

cd /d "%~dp0"

echo ==========================================
echo     Alhrbi Tool - Setup ^& Installer
echo ==========================================
echo.
echo [*] Checking Python installation...
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Python not found! Please install Python (3.10 - 3.13)
    echo [*] Download: https://python.org/downloads
    echo.
    pause
    exit /b 1
)

python --version
echo.
echo ==========================================
echo Choose Installation Type:
echo [1] Self-Bot (discord.py-self)
echo [2] Bot Token (discord.py 2.3.2)
echo ==========================================
echo.
set /p choice="Enter choice (1 or 2, Default is 1): "

if "%choice%"=="" set choice=1

echo.
echo [*] Removing old conflicting discord packages...
pip uninstall -y discord.py discord discord.py-self discord-webhook >nul 2>&1

echo.
if "%choice%"=="2" (
    echo [*] Installing requirements for Bot Token...
    pip install discord.py==2.3.2 colorama aiohttp
) else (
    echo [*] Installing requirements for Self-Bot...
    pip install discord.py-self colorama aiohttp
)

echo.
echo [*] Verifying installation...
echo.

python -c "import discord, colorama, aiohttp; print('[OK] All required packages installed successfully!')" 2>nul

if %errorlevel% neq 0 (
    echo [!] Warning: Verification failed. Attempting fallback installation...
    pip uninstall -y discord.py-self >nul 2>&1
    pip install discord.py==2.3.2 colorama aiohttp
    python -c "import discord, colorama, aiohttp; print('[OK] Fallback installation successful!')" 2>nul
)

echo.
echo ==========================================
echo    Setup completed!
echo ==========================================
echo.
echo [*] To run the tool, open run.bat or type:
echo     python alhrbi.py
echo.
pause
