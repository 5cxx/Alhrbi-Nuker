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

echo [*] Removing old discord packages...
echo.

pip uninstall --quiet -y discord.py discord discord.py-self discord-webhook discord-py 2>nul
pip uninstall --quiet -y discord 2>nul
pip uninstall --quiet -y discord.py 2>nul
pip uninstall --quiet -y discord.py-self 2>nul

echo [OK] Old packages removed
echo.

echo [*] Clearing pip cache...
echo.

pip cache purge 2>nul

echo [OK] Cache cleared
echo.

echo [*] Installing required packages...
echo.

echo [*] Installing discord.py-self...
pip install --quiet --force-reinstall discord.py-self
if %errorlevel% neq 0 (
    echo [X] Failed to install discord.py-self
    echo [*] Trying alternative...
    pip install --quiet --force-reinstall discord.py==2.3.2
)
echo [OK] discord library installed

echo [*] Installing colorama...
pip install --quiet --force-reinstall colorama
echo [OK] colorama installed

echo [*] Installing aiohttp...
pip install --quiet --force-reinstall aiohttp
echo [OK] aiohttp installed

echo.
echo [*] Verifying installation...
echo.

python -c "import discord; print('[OK] discord version:', discord.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo [X] discord verification failed!
    echo [*] Trying to fix...
    python -m pip install --quiet --force-reinstall discord.py-self
)

python -c "import colorama; print('[OK] colorama installed')" 2>nul
python -c "import aiohttp; print('[OK] aiohttp installed')" 2>nul

echo.
echo ==========================================
echo    All packages installed successfully!
echo ==========================================
echo.
echo [*] To run the tool:
echo      - Double click "run.bat"
echo      - Or type: python alhrbi.py
echo.
echo [*] If you get "No module named discord":
echo      - Run this file again as Administrator
echo      - Or manually run: pip install discord.py-self
echo.
pause
