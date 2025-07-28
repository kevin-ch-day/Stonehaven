@echo off
setlocal
cls
echo ====================================================
echo       Stonehaven - Initial Setup Script
echo ====================================================

:: Check for adb.exe
if exist "Utils\Platform_Tools\adb.exe" (
    echo [OK]     adb.exe found in Utils\Platform_Tools
) else (
    echo [ERROR]  adb.exe not found in Utils\Platform_Tools
    echo          Please verify the Android platform-tools are installed correctly.
    pause
    exit /b 1
)

:: Check for sqlite3.exe
if exist "Utils\Platform_Tools\sqlite3.exe" (
    echo [OK]     sqlite3.exe found in Utils\Platform_Tools
) else (
    echo [ERROR]  sqlite3.exe not found in Utils\Platform_Tools
    echo          Please ensure all required tools are present.
    pause
    exit /b 1
)

:: Install Python dependencies
echo.
echo [*]     Installing required Python modules...
pip install colorama
if errorlevel 1 (
    echo [ERROR]  Failed to install colorama. Please install manually.
    pause
    exit /b 1
)

:: Test database connection
echo.
echo [*]     Testing MySQL database connection...
python Database\db_conn.py --test
if errorlevel 1 (
    echo [ERROR]  Database connection test failed.
    echo          Please verify MySQL service is running and credentials are correct.
    pause
    exit /b 1
) else (
    echo [OK]     Database connection established successfully.
)

echo.
echo ====================================================
echo       Setup Complete. You may now run Stonehaven.
echo ====================================================
pause
