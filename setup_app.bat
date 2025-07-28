@echo off
setlocal ENABLEEXTENSIONS
cls

:: ============================================================
::   Stonehaven - Initial Setup Script (ASCII Safe)
:: ============================================================
echo ============================================================
echo         Stonehaven - Initial Setup and Environment Check
echo ============================================================

:: ------------------------------------------------------------
:: Check: adb.exe
:: ------------------------------------------------------------
echo [*] Checking for adb.exe...
if exist "Utils\Platform_Tools\adb.exe" (
    echo [ OK ] adb.exe found in Utils\Platform_Tools
) else (
    echo [FAIL] adb.exe not found in Utils\Platform_Tools
    echo        Please verify Android platform-tools are installed correctly.
    pause
    exit /b 1
)

:: ------------------------------------------------------------
:: Check: sqlite3.exe
:: ------------------------------------------------------------
echo [*] Checking for sqlite3.exe...
if exist "Utils\Platform_Tools\sqlite3.exe" (
    echo [ OK ] sqlite3.exe found in Utils\Platform_Tools
) else (
    echo [FAIL] sqlite3.exe not found in Utils\Platform_Tools
    echo        Please ensure all required tools are present.
    pause
    exit /b 1
)

:: ------------------------------------------------------------
:: Python Check
:: ------------------------------------------------------------
echo [*] Verifying Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Python not detected. Please install Python 3.x and ensure it's in PATH.
    pause
    exit /b 1
) else (
    python --version
)

:: ------------------------------------------------------------
:: Install Python Modules
:: ------------------------------------------------------------
echo.
echo [*] Installing required Python packages...
pip install colorama >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Failed to install 'colorama'. Please install manually using:
    echo        pip install colorama
    pause
    exit /b 1
) else (
    echo [ OK ] Python dependency 'colorama' installed or already present.
)

:: ------------------------------------------------------------
:: Test: MySQL database connection
:: ------------------------------------------------------------
echo.
echo [*] Testing MySQL database connection...
python Database\db_conn.py --test
if errorlevel 1 (
    echo [FAIL] Database connection test failed.
    echo        Please check MySQL service and credentials in db_config.py.
    pause
    exit /b 1
) else (
    echo [ OK ] Database connection established successfully.
)

:: ------------------------------------------------------------
:: Completion Notice
:: ------------------------------------------------------------
echo.
echo ============================================================
echo   Setup Complete. You may now launch the application.
echo ============================================================
pause
endlocal
